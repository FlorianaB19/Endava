import streamlit as st

from chatbot.preference_extractor import (
    UserPreferences,
    extract_preferences,
    merge_preferences,
    has_enough_information,
    get_clarifying_question,
)

from chatbot.recommendation_engine import recommend_breeds

from chatbot.comparison import (
    build_comparison_dataframe,
)

from chatbot.response_generator import (
    generate_recommendation_response,
)


#PAGE CONFIGURATION
st.set_page_config(
    page_title="Dog Breed Recommendation",
    page_icon="🐕",
)

st.title("🐕 Dog Breed Recommendation Assistant")

st.write(
    """
    Tell me about your personality, lifestyle, and what you expect
    from a dog. I will gradually build your preference profile
    and use the project's dataset to find matching breeds.
    """
)

st.info(
    """
    Recommendations are based on the dog breed information
    available in this project's dataset.
    """
)


DEFAULT_USER_PREFERENCES = {  # DEFAULT USER PROFILE
    "preferred_size": None,
    "energy_level": None,
    "barking_level": None,
    "trainability": None,
    "adaptability": None,
    "playfulness": None,
    "openness_to_strangers": None,
    "good_with_children": None,
    "good_with_other_dogs": None,

    # Preference importance
    "size_importance": None,
    "energy_importance": None,
    "barking_importance": None,
    "trainability_importance": None,
    "adaptability_importance": None,
    "playfulness_importance": None,
}


# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []


if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = (
        DEFAULT_USER_PREFERENCES.copy()
    )


if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# HELPER FUNCTIONS
def format_trait_name(trait):
    """
    Convert internal trait names into readable labels.
    """

    labels = {
        "energy_level": "Energy Level",
        "barking_level": "Barking Level",
        "trainability": "Trainability",
        "adaptability": "Adaptability",
        "playfulness": "Playfulness",
        "openness_to_strangers": "Openness to Strangers",
        "good_with_children": "Good with Children",
        "good_with_other_dogs": "Good with Other Dogs",
        "size": "Size",
    }

    return labels.get(
        trait,
        trait.replace("_", " ").title(),
    )


def get_importance_label(importance):
    """
    Convert numeric importance into readable text.
    """

    labels = {
        1: "Nice to have",
        2: "Important",
        3: "Very important",
    }

    return labels.get(
        importance,
        "Important",
    )


def format_trait_value(value):
    """
    Format a numeric dog trait value.
    """

    if value is None:
        return "N/A"

    try:
        numeric_value = float(value)

        if numeric_value.is_integer():
            return f"{int(numeric_value)}/5"

        return f"{numeric_value:.1f}/5"

    except (TypeError, ValueError):
        return str(value)


# BREED CARDS
def render_breed_cards(recommendations):
    """
    Display Top 3 recommendations as visual cards.
    """

    if not recommendations:
        return

    st.subheader(
        "🏆 Your Top Matches"
    )

    columns = st.columns(
        len(recommendations)
    )

    for column, dog in zip(
        columns,
        recommendations,
    ):

        with column:

            breed_name = dog.get(
                "breed",
                "Unknown Breed",
            )

            match_score = dog.get(
                "match_score",
                0,
            )

            calculated_size = dog.get(
                "calculated_size"
            )

            average_weight = dog.get(
                "average_weight"
            )

            energy = dog.get(
                "Energy Level"
            )

            barking = dog.get(
                "Barking Level"
            )

            trainability = dog.get(
                "Trainability Level"
            )

            adaptability = dog.get(
                "Adaptability Level"
            )

            st.markdown(  #breed name
                f"### 🐕 {breed_name}"
            )

            st.metric(  #overall match
                label="Overall Match",
                value=f"{match_score}%",
            )

            progress_value = (
                float(match_score) / 100
            )

            progress_value = min(
                max(
                    progress_value,
                    0.0,
                ),
                1.0,
            )

            st.progress(
                progress_value
            )


            if calculated_size:  #basic information

                st.write(
                    "**Size:** "
                    f"{str(calculated_size).title()}"
                )


            if average_weight is not None:

                try:
                    st.write(
                        "**Average weight:** "
                        f"{float(average_weight):.1f} kg"
                    )
                except (TypeError, ValueError):
                    pass


            st.divider()

            if energy is not None:   #main traits

                st.write(
                    "**Energy:** "
                    f"{format_trait_value(energy)}"
                )


            if barking is not None:

                st.write(
                    "**Barking:** "
                    f"{format_trait_value(barking)}"
                )


            if trainability is not None:

                st.write(
                    "**Trainability:** "
                    f"{format_trait_value(trainability)}"
                )


            if adaptability is not None:

                st.write(
                    "**Adaptability:** "
                    f"{format_trait_value(adaptability)}"
                )



# BREED COMPARISON
def render_breed_comparison(recommendations):
    """
    Display a factual comparison between recommended breeds.

    The comparison uses only dataset information.
    OpenAI is not used to create the table.
    """

    if not recommendations:
        return

    st.subheader(
        "⚖️ Compare Recommended Breeds"
    )

    comparison_df = (
        build_comparison_dataframe(
            recommendations
        )
    )

    if not comparison_df.empty:

        st.dataframe(
            comparison_df,
            use_container_width=True,
        )



    # SELECT SPECIFIC BREEDS
    breed_names = [
        dog.get("breed")
        for dog in recommendations
        if dog.get("breed")
    ]


    if len(breed_names) >= 2:

        st.markdown(
            "#### Select breeds for a focused comparison"
        )

        selected_breeds = st.multiselect(
            "Choose breeds:",
            options=breed_names,
            default=breed_names[:2],
            max_selections=3,
            key="breed_comparison_selector",
        )


        if len(selected_breeds) >= 2:

            selected_recommendations = [
                dog
                for dog in recommendations
                if dog.get("breed")
                in selected_breeds
            ]

            selected_comparison_df = (
                build_comparison_dataframe(
                    selected_recommendations
                )
            )

            st.markdown(
                "#### Selected Comparison"
            )

            st.dataframe(
                selected_comparison_df,
                use_container_width=True,
            )

        else:

            st.caption(
                "Select at least two breeds "
                "to compare them."
            )


# DETAILED MATCH EXPLANATION
def render_match_explanation(recommendations):
    """
    Explain how each recommendation score was calculated.
    """

    if not recommendations:
        return

    st.subheader(
        "📊 Why These Breeds Matched"
    )


    for dog in recommendations:

        breed_name = dog.get(
            "breed",
            "Unknown Breed",
        )

        match_score = dog.get(
            "match_score",
            0,
        )


        with st.expander(
            f"🐕 {breed_name} "
            f"— {match_score}% match"
        ):

            calculated_size = dog.get(  #basic information
                "calculated_size"
            )

            if calculated_size:

                st.write(
                    "**Calculated size:** "
                    f"{str(calculated_size).title()}"
                )


            average_weight = dog.get(
                "average_weight"
            )

            if average_weight is not None:

                try:
                    st.write(
                        "**Average weight:** "
                        f"{float(average_weight):.1f} kg"
                    )
                except (TypeError, ValueError):
                    pass


            st.divider()

            score_details = dog.get(  #score details
                "score_details",
                {},
            )


            for trait, details in (
                score_details.items()
            ):

                trait_label = (
                    format_trait_name(
                        trait
                    )
                )

                score = details.get(
                    "score",
                    0,
                )

                importance = details.get(
                    "importance",
                    2,
                )

                desired_value = details.get(
                    "desired_value"
                )

                actual_value = details.get(
                    "actual_value"
                )


                st.markdown(
                    f"### {trait_label}"
                )

                if trait == "size":       #size

                    st.write(
                        "**Your preference:** "
                        f"{str(desired_value).title()}"
                    )

                    st.write(
                        "**Breed:** "
                        f"{str(actual_value).title()}"
                    )


                else:            #numeric traits

                    st.write(
                        "**Your preference:** "
                        f"{format_trait_value(desired_value)}"
                    )

                    st.write(
                        "**Breed value:** "
                        f"{format_trait_value(actual_value)}"
                    )

                st.write(   #TRAIT MATCH
                    "**Trait match:** "
                    f"{score}%"
                )

                try:

                    progress_value = (
                        float(score) / 100
                    )

                except (TypeError, ValueError):

                    progress_value = 0.0


                progress_value = min(
                    max(
                        progress_value,
                        0.0,
                    ),
                    1.0,
                )

                st.progress(
                    progress_value
                )

                importance_label = (   #importance
                    get_importance_label(
                        importance
                    )
                )

                st.caption(
                    "Preference importance: "
                    f"{importance_label} "
                    f"(weight {importance})"
                )

                st.divider()



# SIDEBAR - USER PROFILE
with st.sidebar:

    st.header(
        "👤 Your Dog Preference Profile"
    )

    profile = (
        st.session_state.user_preferences
    )


    # SIZE
    preferred_size = profile.get(
        "preferred_size"
    )


    if preferred_size:

        st.write(
            "**Preferred size:** "
            f"{preferred_size.title()}"
        )

        size_importance = profile.get(
            "size_importance"
        )

        if size_importance:

            st.caption(
                "Importance: "
                + get_importance_label(
                    size_importance
                )
            )

    else:

        st.write(
            "**Preferred size:** "
            "Not specified"
        )


    # TRAITS
    trait_config = {

        "energy_level": {
            "label": "Energy",
            "importance": "energy_importance",
        },

        "barking_level": {
            "label": "Barking",
            "importance": "barking_importance",
        },

        "trainability": {
            "label": "Trainability",
            "importance": "trainability_importance",
        },

        "adaptability": {
            "label": "Adaptability",
            "importance": "adaptability_importance",
        },

        "playfulness": {
            "label": "Playfulness",
            "importance": "playfulness_importance",
        },

        "openness_to_strangers": {
            "label": "Openness to strangers",
            "importance": None,
        },

        "good_with_children": {
            "label": "Good with children",
            "importance": None,
        },

        "good_with_other_dogs": {
            "label": "Good with other dogs",
            "importance": None,
        },
    }


    for trait, config in (
        trait_config.items()
    ):

        value = profile.get(
            trait
        )

        label = config.get(
            "label"
        )


        if value is None:

            st.write(
                f"**{label}:** "
                "Not specified"
            )

            continue


        st.write(
            f"**{label}:** "
            f"{format_trait_value(value)}"
        )

        try:

            progress_value = (
                float(value) / 5
            )

        except (TypeError, ValueError):

            progress_value = 0.0


        progress_value = min(
            max(
                progress_value,
                0.0,
            ),
            1.0,
        )

        st.progress(
            progress_value
        )


        importance_field = (
            config.get(
                "importance"
            )
        )


        if importance_field:

            importance = profile.get(
                importance_field
            )

            if importance:

                st.caption(
                    "Importance: "
                    + get_importance_label(
                        importance
                    )
                )


    st.divider()


    # RESET PROFILE
    if st.button(   
        "🔄 Reset profile",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.user_preferences = (
            DEFAULT_USER_PREFERENCES.copy()
        )

        st.session_state.recommendations = []

        st.rerun()


for message in (        # CHAT HISTORY
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



user_message = st.chat_input(     # CHAT INPUT
    "Tell me about yourself and your ideal dog..."
)


if user_message:

    st.session_state.messages.append(  #save user messages
        {
            "role": "user",
            "content": user_message,
        }
    )


    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # ASSISTANT
    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Updating your profile..."
        ):

            try:

                new_preferences = (  #extract new preferences
                    extract_preferences(
                        user_message
                    )
                )

                st.session_state.user_preferences = (  #update conversational memory
                    merge_preferences(
                        st.session_state.user_preferences,
                        new_preferences,
                    )
                )

                accumulated_preferences = (  #created structured profile
                    UserPreferences(
                        **st.session_state.user_preferences
                    )
                )

                enough_information = (  #check inormation
                    has_enough_information(
                        st.session_state.user_preferences
                    )
                )


                if not enough_information:  #clarify if necessary

                    answer = (
                        get_clarifying_question(
                            st.session_state.user_preferences
                        )
                    )

                    st.markdown(
                        answer
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                else:

                    recommendations = (  #generate recommendations
                        recommend_breeds(
                            accumulated_preferences,
                            top_n=3,
                        )
                    )


                    st.session_state.recommendations = (
                        recommendations
                    )


                    if not recommendations:

                        answer = (
                            "I could not calculate a recommendation "
                            "from your current profile. "
                            "Please tell me a little more about "
                            "your lifestyle and preferences."
                        )

                        st.markdown(
                            answer
                        )


                    else:

                        answer = (
                            generate_recommendation_response(  #natural laguage explanation
                                user_message=user_message,
                                preferences=accumulated_preferences,
                                recommendations=recommendations,
                            )
                        )

                        st.markdown(
                            answer
                        )


                        render_breed_cards( # top breed cards
                            recommendations
                        )


                        render_breed_comparison( #breed comparison
                            recommendations
                        )

                        render_match_explanation(   #detailed score explanation
                            recommendations
                        )

                    st.session_state.messages.append(  #save assistant response
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )


            except Exception as error:

                st.error(
                    "An error occurred while processing "
                    "your preferences."
                )

                st.exception(
                    error
                )