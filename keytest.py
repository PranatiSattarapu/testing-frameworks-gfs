from anthropic import Anthropic

API_KEY = input("Enter your Anthropic API key: ").strip()

print("\n🔍 Testing Anthropic API key...\n")

try:
    client = Anthropic(api_key=API_KEY)

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hello"}],
    )

    print("✅ SUCCESS — Key is valid!")
    print("Claude responded:", response.content[0].text)

except Exception as e:
    print("❌ ERROR — Key is invalid or not accepted\n")
    print(str(e))
