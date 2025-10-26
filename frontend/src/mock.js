// Mock data for MoodMate frontend

export const mockMessages = {
  'Sad-Turkish': 'Üzgün hissetmek bazen iyileşmenin ilk adımıdır 🌦️',
  'Happy-English': 'Your energy is contagious - keep spreading that light ☀️',
  'Lonely-Spanish': 'Incluso en la soledad, sigues siendo una persona maravillosa 💛',
  'Anxious-English': 'Take a deep breath. You have survived every challenge so far 🌸',
  'Stressed-German': 'Auch Stürme ziehen vorbei. Du schaffst das 💪',
  'Angry-French': 'Ta colère est valide, mais tu es plus fort qu\'elle 🔥',
  'Grateful-Italian': 'La gratitudine è il primo passo verso la gioia 🌻',
  'Overwhelmed-Russian': 'Одна маленькая задача за раз. Ты справишься 🌿',
  'Hopeful-Arabic': 'الأمل هو بداية كل تغيير جميل ✨',
  'Calm-Japanese': 'この静けさを大切に。あなたは素晴らしい 🍃',
  'Neutral-English': 'Every moment is a fresh start waiting to happen 🌅'
};

export const generateMockMessage = (emotion, language) => {
  const key = `${emotion}-${language}`;
  if (mockMessages[key]) {
    return mockMessages[key];
  }
  // Fallback to a generic message
  return 'You are doing great. Keep going! 💙';
};