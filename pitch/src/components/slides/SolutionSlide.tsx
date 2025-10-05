import React from 'react';

export const SolutionSlide = () => (
  <div className="space-y-8">
    <h2 className="text-5xl font-bold text-white mb-8">Єдиний інструмент для повного циклу</h2>
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
      <div className="text-center mb-8">
        <div className="text-3xl font-bold text-green-400 mb-4">Мінімальний бриф</div>
        <div className="text-6xl mb-4">↓</div>
        <div className="text-3xl font-bold text-purple-400 mb-4">AI Processing</div>
        <div className="text-6xl mb-4">↓</div>
        <div className="text-3xl font-bold text-blue-400">Пакет готових креативів</div>
      </div>
      <div className="grid grid-cols-3 gap-4 mt-8">
        <div className="text-center p-4 bg-green-500/20 rounded-lg">
          <div className="text-2xl font-bold text-green-400">Instagram</div>
          <div className="text-sm text-gray-300 mt-2">Stories, Reels, Feed</div>
        </div>
        <div className="text-center p-4 bg-blue-500/20 rounded-lg">
          <div className="text-2xl font-bold text-blue-400">Facebook</div>
          <div className="text-sm text-gray-300 mt-2">Feed, Video Ads</div>
        </div>
        <div className="text-center p-4 bg-purple-500/20 rounded-lg">
          <div className="text-2xl font-bold text-purple-400">TikTok</div>
          <div className="text-sm text-gray-300 mt-2">Vertical Video</div>
        </div>
      </div>
    </div>
  </div>
);

export const solutionSlideConfig = {
  title: "Рішення",
  bg: "bg-gradient-to-br from-green-900 to-blue-900"
};