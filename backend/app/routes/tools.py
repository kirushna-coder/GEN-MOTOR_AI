from flask import Blueprint, jsonify, request
from app.services.gemini import client, ask_gemini_json, ask_gemini

tools_bp = Blueprint('tools', __name__)

@tools_bp.route("/chat", methods=["POST"])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    history = data.get("history", [])

    if not message.strip():
        return jsonify({"status": "error", "message": "Message is required."}), 400

    if not client:
        return jsonify({
            "status": "success", 
            "reply": "This is a mock response. Please add your Gemini API key to the .env file to enable the AI Chat Assistant!"
        })

    # Prepare chat history for Gemini
    formatted_history = "Chat History:\n"
    for msg in history:
        formatted_history += f"{msg.get('role').capitalize()}: {msg.get('content')}\n"
    
    prompt = f"""{formatted_history}
User: {message}
Assistant: """

    try:
        reply = ask_gemini(prompt)
        return jsonify({"status": "success", "reply": reply})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@tools_bp.route("/analyze-resume", methods=["POST"])
def analyze_resume_api():
    data = request.get_json(silent=True) or {}
    role = data.get("role", "General")
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"status": "error", "message": "Please paste your resume text."}), 400

    if not client:
        return jsonify({"status": "success", "data": {
            "score": 85,
            "strengths": [f"Relevant skills for {role}", "Clear formatting"],
            "improvements": ["Add quantifiable metrics", "Expand on project impact"],
            "summary": "This is a mock analysis. Add your Gemini API key to see real AI feedback based on your actual resume!"
        }})

    prompt = f"""You are an expert resume reviewer. Analyze this resume for the role of "{role}".
Resume:
\"\"\"
{text}
\"\"\"
Return your analysis as a JSON object with these exact keys:
- "score": an integer from 0-100 rating the resume
- "strengths": a list of 2-4 strings describing what the resume does well
- "improvements": a list of 2-4 strings describing what needs improvement
- "summary": a 2-3 sentence overall summary
Return ONLY valid JSON, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/generate-roadmap", methods=["POST"])
def generate_roadmap_api():
    data = request.get_json(silent=True) or {}
    role = data.get("role", "Full Stack Developer")
    level = data.get("level", "Beginner")
    timeline = data.get("timeline", "6 months")

    if not client:
        phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        if "3 months" in timeline.lower():
            phases = ["Month 1", "Month 2", "Month 3 (Part 1)", "Month 3 (Part 2)"]
        elif "6 months" in timeline.lower():
            phases = ["Month 1-2", "Month 3-4", "Month 5", "Month 6"]
        elif "1 year" in timeline.lower():
            phases = ["Month 1-3", "Month 4-6", "Month 7-9", "Month 10-12"]
        elif "2 years" in timeline.lower():
            phases = ["Month 1-6", "Month 7-12", "Month 13-18", "Month 19-24"]

        return jsonify({"status": "success", "data": [
            {"phase": phases[0], "title": "Core Fundamentals", "items": ["Programming Basics", "Version Control (Git)", "Command Line"]},
            {"phase": phases[1], "title": f"{role} Specifics", "items": ["Frameworks & Libraries", "Database Design", "API Development"]},
            {"phase": phases[2], "title": "Advanced Topics", "items": ["Cloud Deployment", "Testing & CI/CD", "System Design"]},
            {"phase": phases[3], "title": "Career Prep", "items": ["Portfolio Building", "Mock Interviews", "Apply for Jobs (Mock mode)"]}
        ]})

    prompt = f"""You are a career mentor. Create a step-by-step learning roadmap.
Target Role: {role}
Current Level: {level}
Timeline: {timeline}
Return a JSON array of 4-6 phases. Each phase should have:
- "phase": a time range string like "Month 1-2"
- "title": a short title like "Foundations"
- "items": a list of 3-4 specific skills/topics to learn
Return ONLY a valid JSON array, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/generate-project", methods=["POST"])
def generate_project_api():
    data = request.get_json(silent=True) or {}
    stack = data.get("stack", "Python, React")
    difficulty = data.get("difficulty", "Intermediate")
    domain = data.get("domain", "Any")

    if not client:
        return jsonify({"status": "success", "data": [
            {"icon": "🚀", "title": f"{domain} Dashboard", "desc": f"A {difficulty} level analytics dashboard using {stack}.", "tags": stack.split(",")},
            {"icon": "🤖", "title": "AI Assistant Bot", "desc": "A smart chatbot that helps users automate tasks.", "tags": ["AI/ML", "APIs"]},
            {"icon": "📱", "title": "Mock Application", "desc": "Add your API key to get real project ideas tailored to your stack!", "tags": ["Mock Data"]}
        ]})

    prompt = f"""You are a project idea generator for tech students.
Tech Stack: {stack}
Difficulty: {difficulty}
Domain: {domain}
Generate exactly 3 unique project ideas. Return a JSON array where each item has:
- "icon": a single relevant emoji
- "title": project name (3-5 words)
- "desc": one-sentence project description
- "tags": list of 2-4 technology tags
Return ONLY a valid JSON array, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/generate-project-concept", methods=["POST"])
def generate_project_concept_api():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "Unknown Project")
    desc = data.get("desc", "No description")
    stack = data.get("stack", "Python")

    if not client:
        return jsonify({"status": "success", "data": {
            "explanation": "This is a detailed mock explanation of the project. Please add Gemini API key to get real output.",
            "use_case": "This application can be used by small businesses to manage their inventory efficiently.",
            "problem_statement": "Managing inventory manually leads to human error and data loss.",
            "architecture": "A standard 3-tier architecture with a frontend SPA, a backend API, and a relational database.",
            "tech_stack": [{"name": "Python", "icon": "🐍"}, {"name": "React", "icon": "⚛️"}],
            "folder_structure": "project/\n├── backend/\n│   └── main.py\n└── frontend/\n    └── src/\n        └── App.js",
            "database_schema": {"users": {"id": "int", "name": "string"}, "items": {"id": "int", "name": "string", "quantity": "int"}},
            "api_design": [
                {"endpoint": "/api/users", "method": "GET", "description": "Get all users"},
                {"endpoint": "/api/items", "method": "POST", "description": "Add new item"}
            ],
            "ui_design": "A clean, dark-themed dashboard with glassmorphism elements.",
            "roadmap": ["Phase 1: Foundation", "Phase 2: Core Features", "Phase 3: Deployment"],
            "milestones": ["M1: Backend setup", "M2: Frontend integration", "M3: Beta launch"],
            "future_enhancements": ["Add AI recommendations", "Mobile app version"],
            "references": ["React documentation", "Flask documentation"],
            "modules": ["User Authentication", "Inventory Management", "Analytics Dashboard"]
        }})

    prompt = f"""You are an expert Software Architect and Tech Lead. Create a comprehensive project concept for:
Project Name: {title}
Description: {desc}
Tech Stack: {stack}

Return ONLY a valid JSON object with the following exact keys:
- "explanation": string (Complete project explanation)
- "use_case": string (Real-world use case)
- "problem_statement": string (Problem statement)
- "architecture": string (Solution architecture description)
- "tech_stack": list of objects with "name" and "icon" (Tech stack with icons, use emojis for icons)
- "folder_structure": string (Folder structure representation, use ascii tree format)
- "database_schema": string or object (Database schema design)
- "api_design": list of objects with "endpoint", "method", "description"
- "ui_design": string (UI design preview description)
- "roadmap": list of strings (Development roadmap)
- "milestones": list of strings (Milestones)
- "future_enhancements": list of strings (Future enhancements)
- "references": list of strings (References or useful links)
- "modules": list of strings (List of main modules for source code generation)
Return ONLY valid JSON, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/generate-module-code", methods=["POST"])
def generate_module_code_api():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "Unknown Project")
    stack = data.get("stack", "Python")
    module_name = data.get("module", "Core Module")

    if not client:
        from app.services.gemini import ask_gemini
        return jsonify({"status": "success", "data": f"# Mock Code for {module_name}\\n\\ndef init_{module_name.lower().replace(' ', '_')}():\\n    print('Initialize module')\\n    return True\\n"})

    prompt = f"""You are an expert programmer. Write starting source code for the "{module_name}" module of a project.
Project Name: {title}
Tech Stack: {stack}

Return ONLY the raw code or markdown code block. Include comments explaining the code."""
    from app.services.gemini import ask_gemini
    result = ask_gemini(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/skill-gap", methods=["POST"])
def skill_gap_api():
    data = request.get_json(silent=True) or {}
    current_skills = data.get("skills", "")
    role = data.get("role", "Full Stack Developer")
    experience = data.get("experience", "Fresher")

    if not client:
        readiness = 30
        strengths = [{"name": "Basic Programming", "level": 60}]
        gaps = [{"name": f"Advanced {role} skills", "level": 25}]
        time_est = "6-12 months"
        
        if experience == "1-2 Years":
            readiness = 50
            strengths = [{"name": "Core Programming", "level": 75}, {"name": "Basic APIs", "level": 65}]
            gaps = [{"name": "System Design Basics", "level": 30}, {"name": "Deployment", "level": 40}]
            time_est = "3-6 months"
        elif experience == "3-5 Years":
            readiness = 70
            strengths = [{"name": "System Architecture", "level": 80}, {"name": "Backend Frameworks", "level": 85}]
            gaps = [{"name": "Microservices", "level": 50}, {"name": "Cloud Native (AWS/GCP)", "level": 45}]
            time_est = "2-4 months"
        elif experience == "5+ Years":
            readiness = 90
            strengths = [{"name": "High-Level Architecture", "level": 95}, {"name": "Leadership", "level": 90}]
            gaps = [{"name": "Executive Communication", "level": 60}, {"name": "Advanced Security", "level": 70}]
            time_est = "1-2 months"

        return jsonify({"status": "success", "data": {
            "readiness": readiness,
            "strengths": strengths,
            "gaps": gaps,
            "advice": "This is a dynamic mock result. Please add your Gemini API key to .env for real AI analysis!",
            "weekly_plan": ["Week 1: Fundamentals", "Week 2: Advanced Concepts", "Week 3: Practical Projects", "Week 4: Interview Prep"],
            "courses": [f"Complete {role} Bootcamp (Udemy)", "Advanced System Design (Coursera)"],
            "certifications": [f"Certified {role} Professional", "AWS Certified Developer"],
            "projects": ["Build a mock E-commerce API", "Create a distributed cache system"],
            "interview_topics": ["Data Structures & Algorithms", "System Design", "Behavioral Questions"],
            "time_estimate": time_est
        }})

    prompt = f"""You are a skill assessment expert and career coach.
Current Skills: {current_skills}
Target Role: {role}
Experience Level: {experience}

Analyze the skill gap based on the Experience Level. Ensure realistic expectations:
- Fresher: 20-40% readiness, focus on basics, DSA, Git, SQL, Projects.
- 1-2 Years: 40-60% readiness, focus on APIs, Frameworks, Testing, Deployment.
- 3-5 Years: 60-80% readiness, focus on System Design, Docker, Kubernetes, Cloud, CI/CD.
- 5+ Years: 80-95% readiness, focus on Architecture, Scalability, Microservices, Security, Mentoring.

Return ONLY a valid JSON object with the following exact keys:
- "readiness": an integer 0-100 showing how ready the person is.
- "strengths": a list of objects with "name" (string) and "level" (integer 0-100) for skills they already have.
- "gaps": a list of objects with "name" (string) and "level" (integer 0-100, how much they know) for skills they need to learn. Focus on advanced skills for experienced users.
- "advice": a 2-3 sentence personalized recommendation.
- "weekly_plan": a list of strings describing a week-by-week learning plan (4-6 weeks).
- "courses": a list of strings recommending specific courses or resources.
- "certifications": a list of strings recommending relevant certifications.
- "projects": a list of strings suggesting real-world projects to build.
- "interview_topics": a list of strings with key interview preparation topics.
- "time_estimate": a string indicating the estimated time to reach the target role.

Return ONLY valid JSON, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/mock-interview", methods=["POST"])
def mock_interview_api():
    data = request.get_json(silent=True) or {}
    itype = data.get("type", "Technical")
    topic = data.get("topic", "General Programming")
    count = data.get("count", 5)
    difficulty = data.get("difficulty", "Medium")

    if not client:
        mock_qs = [
            {"q": f"Can you explain the core concepts of {topic}?", "hint": "Think about the fundamentals."},
            {"q": f"Describe a time you faced a difficult problem in {topic}.", "hint": "Use the STAR method."},
            {"q": "(Mock Question) Add your Gemini API key to get real AI-generated questions!", "hint": "Check the .env file."}
        ]
        
        for i in range(4, int(count) + 1):
            mock_qs.append({
                "q": f"Mock Question {i} on {topic} ({difficulty} level)?",
                "hint": f"Think about aspect {i} of {topic}."
            })
            
        return jsonify({"status": "success", "data": mock_qs[:int(count)]})

    prompt = f"""You are an interview coach. Generate {count} interview questions.
Interview Type: {itype}
Topic: {topic}
Difficulty: {difficulty}
Return a JSON array of question objects, each with:
- "q": the question text
- "hint": a short 5-10 word hint
Return ONLY a valid JSON array, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/evaluate-answer", methods=["POST"])
def evaluate_answer_api():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    answer = data.get("answer", "")

    if not client:
        return jsonify({"status": "success", "data": {
            "is_correct": True,
            "score": 7,
            "strengths": ["Good attempt at answering", "Clear communication"],
            "improvements": ["Add specific examples", "Provide more depth"],
            "feedback": "This is a mock evaluation. To get real AI feedback on your answers, please add your Gemini API key!"
        }})

    prompt = f"""You are an interview evaluator. Evaluate this answer.
Question: {question}
Answer: {answer}
Return a JSON object with:
- "is_correct": boolean (whether the answer is fundamentally correct)
- "score": integer 0-10 (rating the quality of the answer)
- "strengths": list of 1-3 short strings (what was good)
- "improvements": list of 1-3 short strings (what to improve)
- "feedback": a 2-3 sentence constructive feedback paragraph
Return ONLY valid JSON, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})


@tools_bp.route("/interview-summary", methods=["POST"])
def interview_summary_api():
    data = request.get_json(silent=True) or {}
    q_and_a = data.get("q_and_a", [])
    
    if not client:
        return jsonify({"status": "success", "data": {
            "overall_strengths": ["Good foundational knowledge", "Clear communication style"],
            "areas_for_improvement": ["Needs more real-world examples", "Dive deeper into advanced topics"],
            "suggested_resources": ["Official Documentation", "Advanced System Design Course"],
            "recommended_topics": ["Data Structures", "Scalability Patterns"],
            "overall_feedback": "This is a mock summary. You did well overall, but adding real-world examples will elevate your performance. Add a Gemini API key for real feedback!"
        }})

    qa_text = ""
    for idx, item in enumerate(q_and_a):
        qa_text += f"Q{idx+1}: {item.get('q')}\nAnswer: {item.get('a')}\n\n"

    prompt = f"""You are an expert interview coach. Review the user's answers to the following interview questions and provide a final summary.
Interview Session:
{qa_text}

Return a JSON object with:
- "overall_strengths": list of 2-4 strings describing their overall strengths.
- "areas_for_improvement": list of 2-4 strings highlighting areas to improve.
- "suggested_resources": list of 2-3 specific learning resources (courses, books, docs).
- "recommended_topics": list of 2-3 specific topics they should practice more.
- "overall_feedback": a concise 2-3 sentence overall assessment.
Return ONLY valid JSON, no markdown or extra text."""

    result = ask_gemini_json(prompt)
    return jsonify({"status": "success", "data": result})
