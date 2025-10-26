# MoodMate Backend Integration Contracts

## API Endpoints

### 1. POST /api/generate-message
Generate an empathetic motivational message based on emotion and language.

**Request:**
```json
{
  "emotion": "Happy",
  "language": "English"
}
```

**Response:**
```json
{
  "message": "Your energy is contagious - keep spreading that light ☀️",
  "emotion": "Happy",
  "language": "English",
  "timestamp": "2025-01-26T10:30:00Z"
}
```

### 2. POST /api/save-message
Save a generated message to user's collection.

**Request:**
```json
{
  "emotion": "Happy",
  "language": "English",
  "message": "Your energy is contagious - keep spreading that light ☀️"
}
```

**Response:**
```json
{
  "id": "uuid",
  "message": "Message saved successfully"
}
```

### 3. GET /api/saved-messages
Retrieve all saved messages (limited to last 50).

**Response:**
```json
{
  "messages": [
    {
      "id": "uuid",
      "emotion": "Happy",
      "language": "English",
      "text": "Your energy is contagious - keep spreading that light ☀️",
      "timestamp": "2025-01-26T10:30:00Z"
    }
  ]
}
```

## MongoDB Collections

### messages
```
{
  _id: ObjectId,
  emotion: String,
  language: String,
  message: String,
  timestamp: DateTime
}
```

## Frontend Changes Required

### Remove Mock Data
- Remove `mock.js` file usage in MoodMate.jsx
- Replace `generateMockMessage()` with API call to `/api/generate-message`

### Update MoodMate Component
- Change `handleGenerate()` to call backend API endpoint
- Update `handleSave()` to call `/api/save-message`
- Add `useEffect()` to load saved messages from `/api/saved-messages` on mount

### API Integration
```javascript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Generate message
const response = await axios.post(`${API}/generate-message`, {
  emotion: selectedEmotion,
  language: selectedLanguage
});

// Save message
await axios.post(`${API}/save-message`, {
  emotion,
  language,
  message
});

// Load saved messages
const response = await axios.get(`${API}/saved-messages`);
```

## AI Integration Details

### LLM Configuration
- Provider: OpenAI
- Model: gpt-4o-mini
- API Key: EMERGENT_LLM_KEY from environment

### Prompt Template
```
You are MoodMate, an empathetic AI that instantly creates short motivational messages.
Your goal is to make the user feel understood, calm, and inspired — like a supportive friend.
Always respond in the selected language: {language}.
The user's current emotion is: {emotion}.
Write a unique 1–2 sentence message that matches their emotion and uplifts them emotionally.
Keep the tone natural, warm, and hopeful. Avoid robotic or overly generic phrases.
Add a small emoji if appropriate, but never more than two.
Return ONLY the message text, nothing else.
```

## Implementation Steps

1. ✅ Install emergentintegrations library
2. ✅ Add EMERGENT_LLM_KEY to backend/.env
3. ✅ Create message generation service with LLM integration
4. ✅ Implement API endpoints in server.py
5. ✅ Create MongoDB models for messages
6. ✅ Update frontend to use real API endpoints
7. ✅ Remove mock.js dependency
8. ✅ Test end-to-end flow
