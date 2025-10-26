import React, { useState, useEffect } from 'react';
import { Heart, Sparkles, Copy, Check } from 'lucide-react';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card, CardContent } from './ui/card';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const emotions = [
  { value: 'Happy', label: '😊 Happy', color: 'from-amber-400 to-orange-400' },
  { value: 'Sad', label: '😢 Sad', color: 'from-blue-400 to-cyan-400' },
  { value: 'Anxious', label: '😰 Anxious', color: 'from-violet-400 to-purple-400' },
  { value: 'Stressed', label: '😫 Stressed', color: 'from-red-400 to-pink-400' },
  { value: 'Angry', label: '😠 Angry', color: 'from-rose-500 to-red-500' },
  { value: 'Lonely', label: '😔 Lonely', color: 'from-slate-400 to-gray-400' },
  { value: 'Grateful', label: '🙏 Grateful', color: 'from-emerald-400 to-teal-400' },
  { value: 'Overwhelmed', label: '😵 Overwhelmed', color: 'from-indigo-400 to-blue-400' },
  { value: 'Hopeful', label: '🌟 Hopeful', color: 'from-yellow-400 to-amber-400' },
  { value: 'Calm', label: '😌 Calm', color: 'from-green-400 to-emerald-400' },
  { value: 'Neutral', label: '😐 Neutral', color: 'from-gray-400 to-slate-400' }
];

const languages = [
  { value: 'English', label: '🇬🇧 English' },
  { value: 'Turkish', label: '🇹🇷 Turkish' },
  { value: 'Spanish', label: '🇪🇸 Spanish' },
  { value: 'German', label: '🇩🇪 German' },
  { value: 'French', label: '🇫🇷 French' },
  { value: 'Italian', label: '🇮🇹 Italian' },
  { value: 'Russian', label: '🇷🇺 Russian' },
  { value: 'Arabic', label: '🇸🇦 Arabic' },
  { value: 'Japanese', label: '🇯🇵 Japanese' }
];

const MoodMate = () => {
  const [selectedEmotion, setSelectedEmotion] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [message, setMessage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [savedMessages, setSavedMessages] = useState([]);

  const handleGenerate = async () => {
    if (!selectedEmotion || !selectedLanguage) {
      toast({
        title: 'Missing information',
        description: 'Please select both an emotion and a language.',
        variant: 'destructive'
      });
      return;
    }

    setIsGenerating(true);
    setIsCopied(false);
    
    // Simulate API call with mock data
    setTimeout(() => {
      const generatedMessage = generateMockMessage(selectedEmotion, selectedLanguage);
      setMessage(generatedMessage);
      setIsGenerating(false);
    }, 800);
  };

  const handleCopy = async () => {
    if (message) {
      await navigator.clipboard.writeText(message);
      setIsCopied(true);
      toast({
        title: 'Copied!',
        description: 'Message copied to clipboard.'
      });
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const handleSave = () => {
    if (message) {
      const newMessage = {
        id: Date.now(),
        emotion: selectedEmotion,
        language: selectedLanguage,
        text: message,
        timestamp: new Date().toISOString()
      };
      setSavedMessages([newMessage, ...savedMessages]);
      toast({
        title: 'Saved!',
        description: 'Message saved successfully.'
      });
    }
  };

  const selectedEmotionData = emotions.find(e => e.value === selectedEmotion);

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-white to-sky-50">
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12 space-y-4">
          <div className="inline-flex items-center gap-2 text-rose-600 mb-2">
            <Heart className="w-8 h-8 fill-current" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-rose-600 to-orange-500 bg-clip-text text-transparent">
              MoodMate
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Your empathetic AI companion that understands your emotions and uplifts your spirit with personalized messages
          </p>
        </div>

        {/* Main Card */}
        <Card className="shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
          <CardContent className="p-8 space-y-6">
            {/* Emotion Selector */}
            <div className="space-y-3">
              <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-rose-500" />
                How are you feeling today?
              </label>
              <Select value={selectedEmotion} onValueChange={setSelectedEmotion}>
                <SelectTrigger className="w-full h-12 text-lg border-2 hover:border-rose-300 transition-colors">
                  <SelectValue placeholder="Select your emotion..." />
                </SelectTrigger>
                <SelectContent>
                  {emotions.map((emotion) => (
                    <SelectItem key={emotion.value} value={emotion.value} className="text-lg py-3">
                      {emotion.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Language Selector */}
            <div className="space-y-3">
              <label className="text-sm font-semibold text-gray-700">
                Choose your language
              </label>
              <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                <SelectTrigger className="w-full h-12 text-lg border-2 hover:border-rose-300 transition-colors">
                  <SelectValue placeholder="Select a language..." />
                </SelectTrigger>
                <SelectContent>
                  {languages.map((lang) => (
                    <SelectItem key={lang.value} value={lang.value} className="text-lg py-3">
                      {lang.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Generate Button */}
            <Button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-rose-500 to-orange-500 hover:from-rose-600 hover:to-orange-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02]"
            >
              {isGenerating ? (
                <span className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 animate-spin" />
                  Generating...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Generate Message
                </span>
              )}
            </Button>

            {/* Message Display */}
            {message && (
              <div className="mt-8 space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div
                  className={`p-8 rounded-2xl bg-gradient-to-br ${selectedEmotionData?.color || 'from-rose-400 to-orange-400'} text-white shadow-xl`}
                >
                  <p className="text-2xl font-medium leading-relaxed text-center">
                    {message}
                  </p>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <Button
                    onClick={handleCopy}
                    variant="outline"
                    className="flex-1 h-12 border-2 hover:bg-gray-50 transition-colors"
                  >
                    {isCopied ? (
                      <span className="flex items-center gap-2">
                        <Check className="w-5 h-5 text-green-600" />
                        Copied!
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        <Copy className="w-5 h-5" />
                        Copy
                      </span>
                    )}
                  </Button>
                  <Button
                    onClick={handleSave}
                    variant="outline"
                    className="flex-1 h-12 border-2 hover:bg-gray-50 transition-colors"
                  >
                    <span className="flex items-center gap-2">
                      <Heart className="w-5 h-5" />
                      Save
                    </span>
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Saved Messages */}
        {savedMessages.length > 0 && (
          <div className="mt-12 space-y-4">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Heart className="w-6 h-6 text-rose-500 fill-current" />
              Saved Messages
            </h2>
            <div className="grid gap-4">
              {savedMessages.map((msg) => {
                const emotionData = emotions.find(e => e.value === msg.emotion);
                return (
                  <Card key={msg.id} className="border-2 hover:shadow-lg transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-sm font-semibold text-gray-500">
                              {emotions.find(e => e.value === msg.emotion)?.label}
                            </span>
                            <span className="text-sm text-gray-400">•</span>
                            <span className="text-sm font-semibold text-gray-500">
                              {languages.find(l => l.value === msg.language)?.label}
                            </span>
                          </div>
                          <p className="text-lg text-gray-700">{msg.text}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MoodMate;