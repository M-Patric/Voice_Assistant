# ==================================================
# KNOWLEDGE SERVICE
# ==================================================

from speech_service import speak


# ==================================================
# LOCAL KNOWLEDGE BASE
# ==================================================

KNOWLEDGE_BASE = {

    "what is python":
        "Python is a high-level programming language "
        "known for its simple syntax and wide range "
        "of applications.",

    "who created python":
        "Python was created by Guido van Rossum "
        "and was first released in 1991.",

    "what is artificial intelligence":
        "Artificial intelligence is the field of "
        "building computer systems that can perform "
        "tasks that normally require human intelligence.",

    "what is machine learning":
        "Machine learning is a branch of artificial "
        "intelligence where computers learn patterns "
        "from data and use those patterns to make "
        "predictions or decisions.",

    "what is an api":
        "An API, or Application Programming Interface, "
        "allows different software applications to "
        "communicate with each other.",

    "what is git":
        "Git is a distributed version control system "
        "used to track changes in source code and "
        "manage software development projects.",

    "what is github":
        "GitHub is a platform for hosting Git "
        "repositories and collaborating on software "
        "development projects.",

    "what is html":
        "HTML stands for HyperText Markup Language. "
        "It is used to structure content on web pages.",

    "what is a database":
        "A database is an organized collection of "
        "information that can be stored, retrieved, "
        "and managed by software.",

    "capital of ghana":
        "The capital city of Ghana is Accra.",

    "what is computer programming":
        "Computer programming is the process of "
        "writing instructions that a computer can "
        "execute to perform specific tasks.",
}


# ==================================================
# ANSWER GENERAL KNOWLEDGE QUESTION
# ==================================================

def answer_general_question(command):
    """
    Searches the local knowledge base for an answer.

    Returns:
        True  -> answer found
        False -> no answer found
    """

    # --------------------------------------------------
    # DIRECT MATCH
    # --------------------------------------------------

    for question, answer in KNOWLEDGE_BASE.items():

        if question in command:

            print(
                "Knowledge base match:",
                question
            )

            speak(answer)

            return True

    # --------------------------------------------------
    # COMMON SPOKEN VARIATIONS
    # --------------------------------------------------

    normalized_command = (
        command
        .replace("what's", "what is")
        .replace("todays", "today's")
    )

    for question, answer in KNOWLEDGE_BASE.items():

        if question in normalized_command:

            print(
                "Knowledge base match:",
                question
            )

            speak(answer)

            return True

    return False


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("Testing knowledge service...")
    print()

    test_commands = [

        "what is python",

        "what's python",

        "tell me what is machine learning",

        "what is artificial intelligence",

        "what is git",

        "what is github",

        "what is an api",

        "what is html",

        "what is a database",

        "what is the capital of ghana",

        "what is computer programming",

        "tell me something that is not in the knowledge base",
    ]

    for command in test_commands:

        print(
            f"Command: {command}"
        )

        found = answer_general_question(
            command
        )

        print(
            f"Answer found: {found}"
        )

        print(
            "-" * 50
        )