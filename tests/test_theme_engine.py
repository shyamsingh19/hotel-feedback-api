def test_theme_grouping():
    from app.theme_engine import group_feedback_by_theme

    feedbacks = [
        "The room was very clean and spotless.",
        "The staff was rude at check-in.",
        "Loved the breakfast.",
        "The pool and spa were relaxing.",
    ]
    themes = group_feedback_by_theme(feedbacks)
    assert len(themes["Cleanliness"]) == 1
    assert len(themes["Staff & Service"]) == 1
    assert len(themes["Food & Dining"]) == 1
    assert len(themes["Amenities"]) == 1
