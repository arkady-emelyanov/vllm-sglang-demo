#!/usr/bin/env python
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

import sys
import threading
import requests
import json
import time
import random
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn


dotenv_file = find_dotenv()
load_dotenv(dotenv_path=dotenv_file)

API_URL = "http://localhost:8080/v1/chat/completions"
MAX_TOKENS = 500
NUM_WORKERS = 5

PROMPTS = [
    "Explain in detail how quantum entanglement can be used to enable ultra-secure communication networks, including examples of practical experiments, potential technological applications, and the theoretical limitations imposed by decoherence and measurement, while comparing it to classical encryption methods.",
    "Provide a comprehensive overview of reinforcement learning algorithms, covering Q-learning, deep Q-networks, policy gradients, actor-critic methods, and their applications in robotics, video games, autonomous driving, and finance, while highlighting the challenges of sample efficiency, reward shaping, and overfitting in high-dimensional environments.",
    "Describe the process of photosynthesis in plants, algae, and cyanobacteria, detailing the light-dependent and light-independent reactions, the roles of chlorophyll a, chlorophyll b, carotenoids, photosystem I and II, electron transport chain, ATP synthase, carbon fixation pathways like C3, C4, and CAM, and explain how environmental factors such as light intensity, CO2 concentration, and temperature affect efficiency.",
    "Summarize the history of artificial intelligence from its inception in the 1950s to modern deep learning breakthroughs, highlighting landmark milestones such as the Turing test, expert systems, backpropagation, convolutional neural networks, generative models, transformers, reinforcement learning in games like AlphaGo, and ethical considerations including bias, transparency, and AI alignment.",
    "Write a detailed short story set in a post-apocalyptic world where humanity relies on AI-controlled ecosystems for survival, describing at least three unique character perspectives, the societal hierarchy, technological innovations like automated agriculture, renewable energy, climate control, and potential conflicts arising from AI decision-making, resource scarcity, and human ambition.",
    "Explain the principles of general relativity, including spacetime curvature, the equivalence principle, geodesics, gravitational time dilation, black holes, gravitational waves, experimental verification through GPS satellite measurements and LIGO observations, and contrast these with Newtonian mechanics in terms of predictive accuracy and conceptual framework.",
    "Provide a step-by-step guide to building a convolutional neural network from scratch in Python, including dataset preprocessing, model architecture, layer types, activation functions, optimization algorithms, loss functions, regularization techniques, evaluation metrics, hyperparameter tuning, and strategies to prevent overfitting and underfitting in high-resolution image classification tasks.",
    "Describe in depth the different types of cryptocurrencies and blockchain consensus mechanisms, including proof of work, proof of stake, delegated proof of stake, proof of authority, and hybrid systems, their impact on scalability, energy efficiency, security, real-world adoption, and regulatory challenges, with examples such as Bitcoin, Ethereum, Cardano, Solana, and Polkadot.",
    "Summarize the major theories in modern cosmology, including Big Bang, inflationary models, dark matter, dark energy, cosmic microwave background radiation, structure formation, galaxy clustering, observational evidence from Planck satellite and Hubble telescope, and ongoing debates such as the Hubble tension and the nature of cosmic acceleration.",
    "Write a highly detailed poem in free verse about the interplay between human consciousness, artificial intelligence, and the universe, including references to neuroscience, quantum mechanics, ethics, technological singularity, memory, perception, and philosophical questions of existence, integrating imagery of stars, networks, neurons, and time.",
    "Explain how CRISPR-Cas9 and related gene editing technologies function at the molecular level, including guide RNA design, Cas protein activity, DNA cleavage, repair mechanisms, off-target effects, ethical concerns, potential applications in medicine, agriculture, and synthetic biology, and the regulatory frameworks governing genome editing research worldwide.",
    "Provide an exhaustive comparison between classical machine learning algorithms like decision trees, random forests, SVMs, k-nearest neighbors, logistic regression, and modern deep learning approaches such as CNNs, RNNs, transformers, and autoencoders, discussing their strengths, limitations, training complexity, data requirements, interpretability, and suitable use cases across industries.",
    "Describe the evolution of human language, from proto-languages to modern linguistic families, highlighting phonetics, morphology, syntax, semantics, pragmatics, historical migration patterns, writing systems, computational linguistics applications, and challenges in machine translation, natural language understanding, and low-resource language preservation.",
    "Explain in detail the concept of dark matter and dark energy, including observational evidence such as galaxy rotation curves, gravitational lensing, cosmic microwave background anisotropies, theoretical candidates like WIMPs, axions, and quintessence, and the implications for cosmology, structure formation, and the ultimate fate of the universe.",
    "Write a long-form story in which a team of scientists travels to a distant exoplanet to investigate signs of alien life, describing planetary conditions, biological hypotheses, technological tools, ethical dilemmas, interpersonal conflicts, and the narrative arc including discoveries, setbacks, and potential first contact scenarios, with multiple subplots interwoven.",
    "Summarize the entire lifecycle of a star, including protostar formation, main-sequence nuclear fusion, red giant phase, planetary nebula, supernova or black hole formation, neutron stars, white dwarfs, nucleosynthesis, and the impact on galactic chemical evolution, with diagrams if possible and comparisons between low-mass and high-mass stellar pathways.",
    "Explain the technical architecture of a transformer-based language model, including input tokenization, embedding layers, positional encodings, multi-head self-attention mechanisms, feed-forward networks, layer normalization, residual connections, pretraining tasks such as masked language modeling, fine-tuning, and common optimization strategies.",
    "Describe the impact of climate change on ecosystems, human societies, global agriculture, water resources, biodiversity, sea-level rise, extreme weather events, and potential mitigation strategies including renewable energy, carbon capture, sustainable farming, international policy agreements, and behavioral change at individual and community levels.",
    "Write a detailed haiku sequence (at least 10 linked haikus) about the evolution of technology from the invention of the wheel to artificial intelligence, integrating historical, philosophical, and futuristic perspectives, and reflecting on human creativity, ambition, and ethical responsibility.",
    "Explain in depth how autonomous vehicles navigate complex urban environments, including sensor fusion with LIDAR, radar, cameras, GPS, SLAM algorithms, path planning, obstacle detection, decision-making under uncertainty, machine learning for perception, edge computing, communication protocols, and regulatory and ethical considerations.",
    "Provide a comprehensive overview of neuroscience, covering neuron structure, action potentials, synaptic transmission, neurotransmitters, brain regions and their functions, neural plasticity, cognitive processes, memory formation, neural networks, neurodegenerative diseases, and techniques such as fMRI, EEG, optogenetics, and computational modeling.",
    "Describe the concept of time from multiple perspectives: physics (relativity, spacetime), philosophy (presentism, eternalism), psychology (perception of duration, memory), biology (circadian rhythms, aging), and technology (synchronization, timekeeping, computational modeling), including paradoxes and unresolved questions.",
    "Explain the mechanics of planetary orbits, Kepler’s laws, Newtonian gravity, perturbations, tidal effects, resonance phenomena, orbital decay, exoplanet detection methods, spacecraft trajectory design, and the role of orbital mechanics in satellite deployment and interplanetary travel, with mathematical formulas where appropriate.",
    "Summarize the evolution of computing hardware, including vacuum tubes, transistors, integrated circuits, microprocessors, GPUs, TPUs, neuromorphic chips, quantum computers, optical computing, memory hierarchy, energy efficiency, parallelization strategies, and the impact of hardware advances on software capabilities and AI development.",
    "Write a long, interconnected narrative that explores the philosophical implications of AI consciousness, featuring multiple characters, dialogue, ethical dilemmas, philosophical arguments, scientific exposition, and speculative technological developments, ensuring narrative coherence while embedding complex technical explanations seamlessly.",
    "Describe the biochemical pathways involved in human metabolism, including glycolysis, Krebs cycle, oxidative phosphorylation, lipid metabolism, amino acid catabolism, hormonal regulation, energy homeostasis, and the implications of metabolic disorders for health, nutrition, and disease management.",
    "Explain in detail the physics of superconductivity, including Cooper pairs, BCS theory, Meissner effect, type I and II superconductors, high-temperature superconductivity, applications in MRI, maglev trains, particle accelerators, and ongoing research challenges in materials science and condensed matter physics.",
    "Provide a detailed comparative analysis of different programming paradigms, including procedural, object-oriented, functional, logic, concurrent, and declarative paradigms, with examples of popular languages, strengths and weaknesses, design patterns, real-world applications, and implications for software engineering and maintainability.",
    "Explain in depth the concept of swarm intelligence, including algorithms inspired by nature such as ant colony optimization, particle swarm optimization, bee algorithms, applications in robotics, traffic optimization, distributed computing, and the challenges of scalability, coordination, and robustness in real-world systems.",
    "Summarize the principles of bioinformatics, covering sequence alignment, genome assembly, transcriptomics, proteomics, structural bioinformatics, systems biology, databases, algorithmic approaches, statistical modeling, machine learning applications, and the integration of computational and experimental biology.",
    "Describe the philosophical and scientific challenges of defining consciousness, including neural correlates, subjective experience, global workspace theory, integrated information theory, functionalist perspectives, panpsychism, ethical implications, and potential future research directions using AI and neuroscience.",
    "Explain the operation and impact of modern wireless communication networks, including 4G, 5G, LTE, MIMO, beamforming, millimeter-wave propagation, network slicing, edge computing, IoT integration, spectrum management, latency reduction, security, and emerging technologies like 6G and terahertz communications.",
    "Write a detailed exploration of the human immune system, covering innate and adaptive immunity, cellular and molecular components, antigen presentation, T and B cell activation, cytokines, immunological memory, vaccine mechanisms, autoimmunity, immunodeficiency, and emerging immunotherapies for cancer and infectious diseases.",
    "Provide an in-depth explanation of how self-supervised learning works in modern AI, including contrastive learning, masked modeling, predictive coding, transformer architectures, data augmentation techniques, evaluation methods, real-world applications in NLP, computer vision, and multimodal systems, along with limitations and open research questions.",
    "Describe the historical and technical evolution of spaceflight, including early rocketry, human space exploration, satellite deployment, interplanetary missions, propulsion technologies, orbital rendezvous, life support systems, space habitats, international collaboration, and future plans for Mars colonization and asteroid mining.",
    "Explain the principles of quantum computing error correction, including qubit decoherence, quantum gates, stabilizer codes, surface codes, fault-tolerant operations, logical qubits, threshold theorems, physical implementations, and implications for scaling up quantum computers for practical applications in cryptography and simulation.",
    "Write a comprehensive overview of the Internet of Things (IoT), including architecture, communication protocols, sensor networks, data analytics, edge computing, cloud integration, security challenges, industrial applications, smart cities, healthcare monitoring, energy management, and future directions for large-scale autonomous systems.",
    "Describe the interplay between economics, technology, and societal change in the digital age, including the rise of AI, automation, cryptocurrencies, global supply chains, labor markets, digital platforms, regulatory challenges, privacy concerns, and ethical considerations for equitable and sustainable technological development.",
    "Explain in detail the principles of fluid dynamics, including Navier-Stokes equations, laminar and turbulent flow, boundary layers, vortices, computational fluid dynamics simulations, applications in aerodynamics, weather prediction, oceanography, and engineering design, with examples illustrating real-world relevance.",
    "Summarize the evolution of human-computer interaction, including early command-line interfaces, graphical user interfaces, touch and gesture interfaces, virtual and augmented reality, natural language interfaces, accessibility considerations, usability testing, cognitive psychology insights, and emerging paradigms in immersive and ubiquitous computing.",
    "Write a speculative story exploring the consequences of AI-driven global decision-making systems on politics, climate change, healthcare, and economics, incorporating detailed technical descriptions of the algorithms, data infrastructure, potential failure modes, ethical debates, and human adaptation strategies in a complex multi-character narrative.",
    "Explain the concept of multiverse theories in cosmology, including the many-worlds interpretation of quantum mechanics, cosmic inflationary multiverse, string theory landscapes, bubble universes, observable consequences, philosophical implications, and critiques from both scientific and philosophical perspectives.",
    "Provide an exhaustive explanation of genetic regulatory networks, including transcription factors, enhancers, repressors, epigenetic modifications, feedback loops, signaling pathways, stochasticity, computational modeling approaches, implications for development, disease, synthetic biology, and bioengineering applications.",
    "Describe in detail how deep generative models like GANs, VAEs, and diffusion models work, including architecture, training objectives, latent space manipulation, applications in image synthesis, text-to-image generation, audio synthesis, potential ethical risks, evaluation metrics, and emerging trends in multimodal generation.",
    "Explain the physics, engineering, and operational principles of fusion energy, including magnetic confinement, inertial confinement, plasma dynamics, tokamaks, stellarators, laser-driven approaches, energy gain challenges, materials considerations, safety, and prospects for commercialization as a sustainable energy source.",
    "Write a long, multi-part haiku series reflecting the evolution of human knowledge from primitive tool-making to modern AI and space exploration, incorporating scientific concepts, philosophical insights, cultural reflections, and environmental awareness, while maintaining poetic cohesion and imagery across all parts.",
    "Provide an in-depth technical explanation of distributed ledger technologies beyond blockchain, including directed acyclic graphs, hashgraph, tangle, consensus protocols, scalability, security considerations, applications in finance, supply chain, healthcare, IoT, and comparisons with traditional centralized and decentralized databases.",
    "Describe the detailed workflow of designing, training, and deploying a large-scale AI model for natural language understanding, including dataset curation, tokenization, architecture selection, pretraining, fine-tuning, evaluation, inference optimization, hardware considerations, ethical review, monitoring, and continuous improvement strategies.",
    "Explain the challenges of modeling complex adaptive systems, including multi-agent interactions, feedback loops, emergent phenomena, network dynamics, computational modeling approaches, sensitivity analysis, validation techniques, applications in ecology, economics, epidemiology, urban planning, and policy-making.",
    "Summarize the complete process of drug discovery and development, including target identification, high-throughput screening, lead optimization, preclinical testing, clinical trials, regulatory approval, pharmacokinetics, pharmacodynamics, computational modeling, personalized medicine, and post-market surveillance.",
    "Write a narrative that interweaves advanced topics in AI, neuroscience, physics, and philosophy into a coherent story exploring human identity, consciousness, and the future of technology, including detailed technical explanations, ethical debates, scientific insights, and multiple character perspectives across different time periods.",
]


def stream_chat(prompt: str, client_id: int, progress, task_id):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": os.getenv("MODEL_PATH"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "max_tokens": MAX_TOKENS,
    }

    with requests.post(API_URL, headers=headers, json=data, stream=True) as response:
        if response.status_code != 200:
            print(response.text)
            sys.exit(1)
            progress.update(task_id, description=f"[red]Client {client_id}: error")
            return

        output = ""
        total_chunks = 0
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            line = line[len("data: "):].strip()
            if line == "[DONE]":
                break
            try:
                chunk = json.loads(line)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    output += delta
                    total_chunks += 1
                    progress.update(task_id, advance=1)
            except Exception:
                continue

        progress.update(task_id, completed=MAX_TOKENS)
        progress.update(task_id, description=f"[green]Client {client_id}: completed.")


def client_loop(client_id, progress, task_id):
    while True:
        prompt = random.choice(PROMPTS)
        progress.update(task_id, description=f"[cyan]Client {client_id}: running...")
        progress.reset(task_id, total=MAX_TOKENS)
        stream_chat(prompt, client_id, progress, task_id)

        time.sleep(random.uniform(1, 3))



def main():
    console = Console()
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
        refresh_per_second=5,
        auto_refresh=True,
    ) as progress:
        tasks = [progress.add_task(f"Client {i}: idle", total=100) for i in range(NUM_WORKERS)]

        threads = [
            threading.Thread(target=client_loop, args=(i, progress, tasks[i]), daemon=True)
            for i in range(NUM_WORKERS)
        ]

        try:
            for t in threads:
                t.start()

            for t in threads:
                t.join()        
            
        except KeyboardInterrupt:
            console.print("[yellow]\nStopped by user.")
            sys.exit(0)


if __name__ == "__main__":
    main()
