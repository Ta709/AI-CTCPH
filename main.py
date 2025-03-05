import requests
import re

# Load API Keys securely from a file
def load_api_keys(file_path="api_keys.txt"):
    keys = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                keys[key] = value
    except Exception as e:
        print(f"⚠️ Error loading API keys: {e}")
    return keys

api_keys = load_api_keys()
api_key = api_keys.get("GOOGLE_API_KEY", "")
cse_id = api_keys.get("GOOGLE_CSE_ID", "")

# Memory for conversation context
chat_memory = []

# 🔎 **Function to Perform Google Search**
def google_search(query, num_results=3):
    if not api_key or not cse_id:
        return "⚠️ **API keys are missing!** Please check `api_keys.txt`."

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses (e.g., 403, 500)
        search_results = response.json()

        if "items" in search_results:
            summary = "\n📌 **Here’s what I found:**\n"
            for i, result in enumerate(search_results["items"][:num_results], start=1):
                title = result["title"]
                snippet = result["snippet"]
                link = result["link"]
                summary += f"\n🔹 **{i}. {title}**\n   📝 {snippet}\n   🔗 [Read more]({link})\n"
            return summary
        else:
            return "❌ **No relevant search results found.**"

    except requests.exceptions.RequestException as e:
        return f"⚠️ **Error retrieving data:** {e}"

# 🧮 **Function to Solve Math Problems**
def solve_math(expression):
    try:
        if "%" in expression:
            match = re.match(r"(\d+)%\s*of\s*(\d+)", expression)
            if match:
                percent = int(match.group(1))
                number = int(match.group(2))
                return f"✅ **{percent}% of {number}** = `{percent / 100 * number}`"

        return f"✅ **Solution:** `{eval(expression)}`"

    except Exception:
        return "❌ **I couldn't solve that.** Please try a different format."

# 🗣 **Chatbot Response Handler**
def chatbot_response(user_input):
    global chat_memory
    user_input = user_input.lower().strip()

    # Handle Greetings
    if user_input in ["hi", "hello", "hey"]:
        return "👋 **Hello! How can I assist you today?**"

    # Handle Farewells
    if user_input in ["bye", "goodbye"]:
        return "👋 **Goodbye! Have a great day!**"

    # Check for math expressions
    if re.search(r"\d", user_input):
        math_answer = solve_math(user_input)
        if "I couldn't solve" not in math_answer:
            return math_answer

    # Web search for general knowledge questions
    chat_memory.append(user_input)
    return google_search(user_input)

# 🚀 **Start Chatbot**
def start_chat():
    print("🤖 **AI Chatbot:** Hello! Ask me anything. Type 'bye' to exit.")

    while True:
        user_input = input("💬 **You:** ")
        if user_input.lower() == "bye":
            print("🤖 **AI Chatbot:** Goodbye! 👋")
            break
        response = chatbot_response(user_input)
        print(f"\n{response}\n")

# Run chatbot
if __name__ == "__main__":
    start_chat()
