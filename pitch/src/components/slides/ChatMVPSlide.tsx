import React from 'react';
import { CheckCircle } from 'lucide-react';
import { ChatDemoButton } from '../DemoButton';

export const ChatMVPSlide = () => (
  <div className="space-y-6">
    <div className="bg-purple-500/20 rounded-xl p-2 inline-block">
      <span className="text-purple-400 font-bold text-xl px-4">STEP 2</span>
    </div>
    <h2 className="text-5xl font-bold text-white">Інтелектуальний збір брифу + генерація</h2>
    <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-purple-500/30">
      <div className="space-y-6">
        <div className="flex items-start gap-4">
          <div className="bg-purple-500 rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0 text-white font-bold">1</div>
          <div>
            <h3 className="text-xl font-semibold text-purple-400 mb-2">Conversational UI</h3>
            <p className="text-gray-300">Діалоговий збір даних з адаптивними питаннями</p>
          </div>
        </div>
        <div className="flex items-start gap-4">
          <div className="bg-purple-500 rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0 text-white font-bold">2</div>
          <div>
            <h3 className="text-xl font-semibold text-purple-400 mb-2">Pattern-based suggestions</h3>
            <p className="text-gray-300">Пропозиції на основі успішних кейсів зі Step 1</p>
          </div>
        </div>
        <div className="flex items-start gap-4">
          <div className="bg-purple-500 rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0 text-white font-bold">3</div>
          <div>
            <h3 className="text-xl font-semibold text-purple-400 mb-2">Platform presets</h3>
            <p className="text-gray-300">Auto-налаштування формату, тривалості, CTA під платформу</p>
          </div>
        </div>
        <div className="flex items-start gap-4">
          <div className="bg-purple-500 rounded-full w-10 h-10 flex items-center justify-center flex-shrink-0 text-white font-bold">4</div>
          <div>
            <h3 className="text-xl font-semibold text-purple-400 mb-2">Video generation</h3>
            <p className="text-gray-300">TTS озвучка + автомонтаж (ffmpeg) + експорт у хмару</p>
          </div>
        </div>
      </div>
    </div>
    <div className="bg-green-500/20 rounded-xl p-4 border border-green-400/30">
      <div className="flex items-center justify-between">
        <p className="text-lg text-white flex items-center gap-3">
          <CheckCircle className="w-6 h-6 text-green-400" />
          <span className="font-semibold">✅ Вже реалізовано: Chat MVP Pro повністю працює</span>
        </p>
        <ChatDemoButton 
          variant="primary" 
          size="md" 
          showDescription={false}
        />
      </div>
    </div>
  </div>
);

export const chatMVPSlideConfig = {
  title: "Step 2: Chat MVP Pro",
  bg: "bg-gradient-to-br from-purple-900 to-pink-900"
};