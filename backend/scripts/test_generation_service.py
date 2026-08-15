from app.modules.generation.services.generation_service import GenerationService


generation_service = GenerationService()


context = """
Meditation is described as a way to refine and use
the energy generated through the practice.

The text explains that meditation helps transform
the generated energy and is an important part of
the training.
"""

question = "What is the purpose of meditation?"


answer = generation_service.generate(
    question=question,
    context=context,
)


print("\n===== GENERATED ANSWER =====\n")
print(answer)