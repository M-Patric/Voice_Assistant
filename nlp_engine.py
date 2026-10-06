# ==================================================
# NLP INTENT ENGINE
# ==================================================

import nltk

from nltk.tokenize import wordpunct_tokenize

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.pipeline import FeatureUnion

from sklearn.linear_model import LogisticRegression


# ==================================================
# NLP TRAINING DATA
# ==================================================

TRAINING_DATA = [

    # --------------------------------------------------
    # GREETING
    # --------------------------------------------------

    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hi there", "greeting"),
    ("hey", "greeting"),
    ("hey assistant", "greeting"),
    ("hello assistant", "greeting"),
    ("good morning", "greeting"),
    ("good afternoon", "greeting"),
    ("good evening", "greeting"),
    ("hello how are you", "greeting"),
    ("hey how are you", "greeting"),
    ("nice to meet you", "greeting"),
    ("are you there", "greeting"),
    ("can you hear me", "greeting"),
    ("i am here", "greeting"),

    # --------------------------------------------------
    # TIME
    # --------------------------------------------------

    ("what time is it", "time"),
    ("tell me the time", "time"),
    ("what is the current time", "time"),
    ("can you tell me the time", "time"),
    ("do you know what time it is", "time"),
    ("what time is it right now", "time"),
    ("could you tell me the current hour", "time"),
    ("please tell me the time", "time"),
    ("what is the time right now", "time"),
    ("can you tell me what time it is", "time"),
    ("may i know the current time", "time"),
    ("what hour is it", "time"),

    # --------------------------------------------------
    # DATE
    # --------------------------------------------------

    ("what is today's date", "date"),
    ("tell me today's date", "date"),
    ("what date is it", "date"),
    ("what day is it today", "date"),
    ("can you tell me the date", "date"),
    ("do you know today's date", "date"),
    ("what is the current date", "date"),
    ("please tell me today's date", "date"),
    ("what day are we on", "date"),
    ("what is the date today", "date"),
    ("can you tell me what today's date is", "date"),

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    ("search python programming", "search"),
    ("search for python tutorials", "search"),
    ("look up python programming", "search"),
    ("find information about machine learning", "search"),
    ("search the internet for python", "search"),
    ("look for programming tutorials", "search"),
    ("search for information", "search"),
    ("look something up", "search"),
    ("search online", "search"),
    ("find this on the internet", "search"),
    ("can you search the web", "search"),
    ("please look up something", "search"),
    ("find information online", "search"),
    ("search the internet", "search"),

    # --------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------

    ("open youtube", "open_youtube"),
    ("launch youtube", "open_youtube"),
    ("go to youtube", "open_youtube"),
    ("please open youtube", "open_youtube"),
    ("can you launch youtube", "open_youtube"),
    ("take me to youtube", "open_youtube"),
    ("open the youtube website", "open_youtube"),
    ("i want youtube", "open_youtube"),
    ("please launch youtube", "open_youtube"),

    # --------------------------------------------------
    # GOOGLE
    # --------------------------------------------------

    ("open google", "open_google"),
    ("launch google", "open_google"),
    ("go to google", "open_google"),
    ("please open google", "open_google"),
    ("can you launch google", "open_google"),
    ("take me to google", "open_google"),
    ("open the google website", "open_google"),
    ("i want google", "open_google"),
    ("please launch google", "open_google"),

    # --------------------------------------------------
    # GITHUB
    # --------------------------------------------------

    ("open github", "open_github"),
    ("launch github", "open_github"),
    ("go to github", "open_github"),
    ("please open github", "open_github"),
    ("can you launch github", "open_github"),
    ("take me to github", "open_github"),
    ("open the github website", "open_github"),
    ("i want github", "open_github"),
    ("please launch github", "open_github"),

    # --------------------------------------------------
    # REMINDER
    # --------------------------------------------------

    ("set a reminder", "reminder"),
    ("set a reminder for ten seconds", "reminder"),
    ("remind me in ten seconds", "reminder"),
    ("remind me in five minutes", "reminder"),
    ("can you remind me later", "reminder"),
    ("set a timer reminder", "reminder"),
    ("please remind me", "reminder"),
    ("i want to set a reminder", "reminder"),
    ("remind me about something", "reminder"),
    ("set a reminder for later", "reminder"),
    ("can you set a timer", "reminder"),

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    ("what is the weather in accra", "weather"),
    ("what's the weather in kumasi", "weather"),
    ("tell me the weather in takoradi", "weather"),
    ("what is the weather like in accra", "weather"),
    ("can you check the weather in accra", "weather"),
    ("how is the weather in kumasi", "weather"),
    ("what is the temperature in accra", "weather"),
    ("what is the weather in ghana", "weather"),
    ("tell me today's weather", "weather"),
    ("check the weather", "weather"),
    ("can you check today's weather", "weather"),
    ("what is the temperature outside", "weather"),
    ("how is the weather today", "weather"),
    ("give me the weather forecast", "weather"),
    ("please check the weather", "weather"),

    # --------------------------------------------------
    # EMAIL
    # --------------------------------------------------

    ("send an email", "email"),
    ("send an email to someone", "email"),
    ("compose an email", "email"),
    ("write an email", "email"),
    ("send email", "email"),
    ("i want to send an email", "email"),
    ("please send an email", "email"),
    ("i need to send an email", "email"),
    ("can you send an email", "email"),
    ("help me send an email", "email"),
    ("compose an email for me", "email"),
    ("i want to compose an email", "email"),

    # --------------------------------------------------
    # KNOWLEDGE
    # --------------------------------------------------

    ("what is python", "knowledge"),
    ("who created python", "knowledge"),
    ("what is machine learning", "knowledge"),
    ("what is artificial intelligence", "knowledge"),
    ("what is an api", "knowledge"),
    ("what is git", "knowledge"),
    ("what is github", "knowledge"),
    ("what is html", "knowledge"),
    ("what is a database", "knowledge"),
    ("what is the capital of ghana", "knowledge"),
    ("tell me about python", "knowledge"),
    ("what is computer programming", "knowledge"),
    ("explain python", "knowledge"),
    ("tell me about machine learning", "knowledge"),
    ("explain artificial intelligence", "knowledge"),
    ("what does api mean", "knowledge"),
    ("what does git do", "knowledge"),

    # --------------------------------------------------
    # GOODBYE
    # --------------------------------------------------

    ("goodbye", "goodbye"),
    ("goodbye assistant", "goodbye"),
    ("quit", "goodbye"),
    ("exit", "goodbye"),
    ("please shut down", "goodbye"),
    ("stop the assistant", "goodbye"),
    ("close the assistant", "goodbye"),
    ("turn yourself off", "goodbye"),
    ("i am done", "goodbye"),
    ("see you later", "goodbye"),
    ("stop listening", "goodbye"),

    # --------------------------------------------------
    # UNKNOWN / UNRELATED
    # --------------------------------------------------

    ("play a game", "unknown"),
    ("tell me a joke", "unknown"),
    ("what is my favorite color", "unknown"),
    ("make me breakfast", "unknown"),
    ("book me a flight", "unknown"),
    ("turn on the television", "unknown"),
    ("dance for me", "unknown"),
    ("sing a song", "unknown"),
    ("tell me a story", "unknown"),
    ("order some food", "unknown"),
    ("send a text message", "unknown"),
    ("buy something online", "unknown"),
]


# ==================================================
# TEXT PREPROCESSING
# ==================================================

def preprocess_text(text):
    """
    Normalizes and tokenizes text before it is
    passed to the machine-learning model.
    """

    text = text.lower().strip()

    tokens = wordpunct_tokenize(text)

    return " ".join(tokens)


# ==================================================
# TRAIN NLP INTENT CLASSIFIER
# ==================================================

def train_intent_classifier():
    """
    Trains the local NLP intent classification model.

    The model combines:
        1. Word-level TF-IDF features
        2. Character-level TF-IDF features
        3. Logistic Regression

    Returns:
        vectorizer, classifier
    """

    training_sentences = [
        preprocess_text(sentence)
        for sentence, intent in TRAINING_DATA
    ]

    training_labels = [
        intent
        for sentence, intent in TRAINING_DATA
    ]

    # --------------------------------------------------
    # WORD-LEVEL FEATURES
    # --------------------------------------------------

    word_vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    # --------------------------------------------------
    # CHARACTER-LEVEL FEATURES
    # --------------------------------------------------

    character_vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        sublinear_tf=True
    )

    # --------------------------------------------------
    # COMBINE BOTH FEATURE TYPES
    # --------------------------------------------------

    vectorizer = FeatureUnion([
        ("word", word_vectorizer),
        ("character", character_vectorizer)
    ])

    training_vectors = vectorizer.fit_transform(
        training_sentences
    )

    # --------------------------------------------------
    # TRAIN CLASSIFIER
    # --------------------------------------------------

    classifier = LogisticRegression(
        max_iter=3000,
        C=3.0,
        class_weight=None
    )

    classifier.fit(
        training_vectors,
        training_labels
    )

    print(
        "NLP intent classifier trained successfully."
    )

    print(
        f"Training examples: {len(TRAINING_DATA)}"
    )

    print(
        f"Detected intent classes: "
        f"{len(classifier.classes_)}"
    )

    return vectorizer, classifier


# ==================================================
# TRAIN MODEL WHEN MODULE LOADS
# ==================================================

vectorizer, intent_classifier = (
    train_intent_classifier()
)


# ==================================================
# PREDICT INTENT
# ==================================================

def predict_intent(command):
    """
    Predicts the user's intent.

    Returns:
        intent,
        confidence,
        margin
    """

    processed_command = preprocess_text(
        command
    )

    command_vector = vectorizer.transform(
        [processed_command]
    )

    probabilities = (
        intent_classifier
        .predict_proba(command_vector)[0]
    )

    sorted_probabilities = sorted(
        probabilities,
        reverse=True
    )

    best_index = probabilities.argmax()

    intent = (
        intent_classifier
        .classes_[best_index]
    )

    confidence = probabilities[best_index]

    # Difference between the best prediction and
    # the second-best prediction.
    if len(sorted_probabilities) > 1:
        margin = (
            sorted_probabilities[0]
            - sorted_probabilities[1]
        )
    else:
        margin = confidence

    return intent, confidence, margin


# ==================================================
# INTENT DECISION
# ==================================================

def classify_intent(
    command,
    confidence_threshold=0.45,
    margin_threshold=0.10
):
    """
    Classifies a command and applies confidence
    and prediction-margin safeguards.

    Returns:
        final_intent,
        confidence,
        margin
    """

    intent, confidence, margin = (
        predict_intent(command)
    )

    print(
        f"Intent confidence: "
        f"{confidence:.2f}"
    )

    print(
        f"Intent margin: "
        f"{margin:.2f}"
    )

    # Reject weak predictions.
    if confidence < confidence_threshold:
        return "unknown", confidence, margin

    # Reject ambiguous predictions.
    if margin < margin_threshold:
        return "unknown", confidence, margin

    return intent, confidence, margin


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("Testing NLP engine...")
    print()

    test_commands = [
        "hello",
        "could you tell me what's the current time",
        "please tell me what today's date is",
        "can you open youtube for me",
        "would you search the internet for python",
        "please check the weather in Accra",
        "i would like to send an email",
        "what is machine learning",
        "goodbye",
        "tell me a joke",
    ]

    for command in test_commands:

        intent, confidence, margin = (
            classify_intent(command)
        )

        print(
            f"Command: {command}"
        )

        print(
            f"Detected: {intent}"
        )

        print(
            f"Confidence: {confidence:.2f}"
        )

        print(
            f"Margin: {margin:.2f}"
        )

        print("-" * 50)