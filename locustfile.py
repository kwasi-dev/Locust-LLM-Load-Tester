from locust import HttpUser, task, between
import json
import random
import os

API_KEY = os.getenv("LOCUST_API_KEY")
TARGET_MODEL = os.getenv("TARGET_MODEL")

PROMPTS = [
    "Write a 500 word essay analyzing the long-term impact of artificial intelligence on global economics.",
    "Write a 500 word essay discussing climate change adaptation strategies for small island developing states.",
    "Write a 500 word essay on the historical evolution of democracy from ancient Athens to modern states.",
    "Write a 500 word essay evaluating the ethics of genetic engineering in humans.",
    "Write a 500 word essay explaining the socio-economic consequences of the Industrial Revolution.",
    "Write a 500 word essay exploring the psychological effects of social media on teenagers.",
    "Write a 500 word essay on renewable energy adoption across the Caribbean.",
    "Write a 500 word essay analyzing the philosophy of existentialism with examples.",
    "Write a 500 word essay discussing cybersecurity threats in modern enterprises.",
    "Write a 500 word essay on quantum computing and its potential applications.",
    "Write a 500 word essay explaining blockchain technology for non-technical readers.",
    "Write a 500 word essay about the rise and influence of the Roman Empire.",
    "Write a 500 word essay discussing migration patterns in the 21st century.",
    "Write a 500 word essay evaluating the pros and cons of nuclear power.",
    "Write a 500 word essay on the global food security crisis.",
    "Write a 500 word essay describing the evolution of mobile computing.",
    "Write a 500 word essay analyzing Shakespeare’s influence on modern literature.",
    "Write a 500 word essay on the psychology of motivation in the workplace.",
    "Write a 500 word essay explaining how machine learning models are trained.",
    "Write a 500 word essay discussing the future of space exploration.",
    "Write a 500 word essay evaluating the education system in developing countries.",
    "Write a 500 word essay on the ethical concerns of autonomous weapons.",
    "Write a 500 word essay explaining how global supply chains operate.",
    "Write a 500 word essay detailing the history of the internet.",
    "Write a 500 word essay on the rise of fintech and digital payments.",
    "Write a 500 word essay analyzing feminist movements across the 20th century.",
    "Write a 500 word essay discussing mental health challenges in modern society.",
    "Write a 500 word essay on the impact of colonialism on Caribbean culture.",
    "Write a 500 word essay evaluating public transportation systems around the world.",
    "Write a 500 word essay on the philosophy of Stoicism and its relevance today.",
    "Write a 500 word essay discussing AI ethics and bias in large language models.",
    "Write a 500 word essay about the global water scarcity crisis.",
    "Write a 500 word essay explaining the rise of e-commerce.",
    "Write a 500 word essay on biodiversity loss and conservation strategies.",
    "Write a 500 word essay analyzing leadership styles in modern companies.",
    "Write a 500 word essay discussing poverty reduction strategies.",
    "Write a 500 word essay on the evolution of transportation technology.",
    "Write a 500 word essay about the causes of World War II.",
    "Write a 500 word essay explaining the science of hurricanes.",
    "Write a 500 word essay on the challenges facing the healthcare sector.",
    "Write a 500 word essay analyzing the economics of cryptocurrency.",
    "Write a 500 word essay discussing artificial general intelligence.",
    "Write a 500 word essay on childhood development and education.",
    "Write a 500 word essay explaining how to design secure REST APIs.",
    "Write a 500 word essay on urbanization in developing nations.",
    "Write a 500 word essay evaluating the impact of tourism on small island economies.",
    "Write a 500 word essay discussing political polarization in modern democracies.",
    "Write a 500 word essay on the history of mathematics.",
    "Write a 500 word essay analyzing the global financial crisis of 2008.",
    "Write a 500 word essay explaining the ethics of data privacy.",
    "Write a 500 word essay describing the evolution of computer graphics.",
    "Write a 500 word essay on sustainable agriculture practices.",
    "Write a 500 word essay analyzing conflict resolution strategies.",
    "Write a 500 word essay discussing smart cities of the future.",
    "Write a 500 word essay on the psychology of addiction.",
    "Write a 500 word essay explaining deep learning neural networks.",
    "Write a 500 word essay on transportation logistics optimization.",
    "Write a 500 word essay evaluating global responses to pandemics.",
    "Write a 500 word essay analyzing the ethics of digital surveillance.",
    "Write a 500 word essay on historical scientific discoveries that changed the world.",
    "Write a 500 word essay discussing machine automation in industry.",
    "Write a 500 word essay on the future of higher education.",
    "Write a 500 word essay exploring Caribbean folklore and mythology.",
    "Write a 500 word essay about the impact of music on human cognition.",
    "Write a 500 word essay analyzing voting systems around the world.",
    "Write a 500 word essay discussing the philosophy of utilitarianism.",
    "Write a 500 word essay on global shipping and maritime trade.",
    "Write a 500 word essay explaining the science of climate change.",
    "Write a 500 word essay analyzing the ethics of social credit systems.",
    "Write a 500 word essay on artificial intelligence in healthcare.",
    "Write a 500 word essay discussing the history of space flight.",
    "Write a 500 word essay on renewable energy storage technology.",
    "Write a 500 word essay explaining the psychology behind decision-making.",
    "Write a 500 word essay analyzing the rise of decentralized finance.",
    "Write a 500 word essay on Caribbean cultural identity.",
    "Write a 500 word essay discussing strategies for reducing income inequality.",
    "Write a 500 word essay explaining natural language processing.",
    "Write a 500 word essay about ethical leadership.",
    "Write a 500 word essay on global trade agreements.",
    "Write a 500 word essay analyzing transportation emissions.",
    "Write a 500 word essay discussing the importance of critical thinking.",
    "Write a 500 word essay on the neuroscience of learning.",
    "Write a 500 word essay explaining how the justice system works.",
    "Write a 500 word essay evaluating ethical issues in biotechnology.",
    "Write a 500 word essay analyzing political corruption.",
    "Write a 500 word essay discussing the challenges of digital transformation in traditional businesses.",
    "Write a 500 word essay on internet censorship.",
    "Write a 500 word essay exploring the cultural impact of cinema.",
    "Write a 500 word essay analyzing the rise of AI-driven automation.",
    "Write a 500 word essay on Caribbean carnival traditions.",
    "Write a 500 word essay discussing the future of remote work.",
    "Write a 500 word essay explaining econometrics for beginners.",
    "Write a 500 word essay analyzing quantum physics principles.",
    "Write a 500 word essay on global population growth challenges."
]

class LLMUser(HttpUser):
    wait_time = between(2, 5)

    @task
    def query_llm(self):
        prompt = random.choice(PROMPTS)

        payload = {
            "model": TARGET_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 5000,
            "temperature": 0.7,
            "stream": True,
        }
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        
        with self.client.post(
            "/api/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            stream=True, 
            catch_response=True,
            name="chat-stream"
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            try:
                # Read streaming chunks
                for line in response.iter_lines():
                    if not line:
                        continue

                    # OpenAI-compatible streams send "data: {...}"
                    if line.startswith(b"data: "):
                        data = line.replace(b"data: ", b"")
                        if data.strip() == b"[DONE]":
                            break

                response.success()
            except Exception as e:
                response.failure(f"Stream error: {e}")
