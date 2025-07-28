student_madlibs = [
    { 'name': 'Open Prompt',
     'template': '{input_text}',
        'variables': ['input_text'],
        'descriptions': [''],
        'placeholders': ['Message AI chatbot...']
    }, {'name': 'Metaphor',
        'template': "I'm having trouble understanding {concept}. Please explain it as a metaphor",
        'variables': ['concept'],
        'descriptions': ["I'm having trouble understanding"],
        'placeholders': ['']
    }, {'name': 'Step-by-Step',
        'template': "I'm having trouble understanding {concept}. Please help me break it down into steps.",
        'variables': ['concept'],
        'descriptions': ["I'm having trouble understanding"],
        'placeholders': ['']
    }, {'name': 'Debate Partner',
        'template': "I want to debate about {concept}. Let's use the Socratic method. You are subject matter expert who is trying to convince me about it.  You will speak first  and then wait for me to respond.",
        'variables': ['concept'],
        'descriptions': ["I want to debate about"],
        'placeholders': ['']
    }
]

educator_madlibs = [
    { 'name': 'Open Prompt',
     'template': '{input_text}',
        'variables': ['input_text'],
        'descriptions': [''],
        'placeholders': ['Message AI chatbot...']
    }, {'name': 'Metaphor',
        'template': "I'm having trouble understanding {concept}. Please explain it as a metaphor",
        'variables': ['concept'],
        'descriptions': ["I'm having trouble understanding"],
        'placeholders': ['']
    }, {'name': 'Translate',
        'template': "Help me translate the following text into {language}: {text}",
        'variables': ['language', 'text'],
        'descriptions': ["Text", "Language"],
        'placeholders': ['', '']
    }, {'name': 'Quiz Questions',
        'template': "Help me generate 10 quiz questions about {concept}.",
        'variables': ['concept'],
        'descriptions': ["Quiz Topic"],
        'placeholders': ['']
    }
] 