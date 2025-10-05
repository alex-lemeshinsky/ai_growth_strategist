import React from 'react';

export const RoadmapSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Наступні 2-4 тижні</h2>
    <div className="space-y-4">
      <div className="bg-green-500/20 rounded-xl p-6 border-l-4 border-green-500">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-2xl font-semibold text-white">Тиждень 1: Video Generation Engine</h3>
          <span className="text-green-400 font-bold">Priority 1</span>
        </div>
        <ul className="space-y-2 text-gray-300 ml-4">
          <li>TTS integration (OpenAI/ElevenLabs)</li>
          <li>FFmpeg pipeline для монтажу</li>
          <li>S3 upload + CDN</li>
        </ul>
      </div>
      <div className="bg-blue-500/20 rounded-xl p-6 border-l-4 border-blue-500">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-2xl font-semibold text-white">Тиждень 2: Global Patterns DB</h3>
          <span className="text-blue-400 font-bold">Priority 2</span>
        </div>
        <ul className="space-y-2 text-gray-300 ml-4">
          <li>Таксономія патернів</li>
          <li>Семантичний пошук (embeddings)</li>
          <li>Крос-кейсові рекомендації</li>
        </ul>
      </div>
      <div className="bg-purple-500/20 rounded-xl p-6 border-l-4 border-purple-500">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-2xl font-semibold text-white">Тиждень 3: Policy Fix-it Automation</h3>
          <span className="text-purple-400 font-bold">Priority 3</span>
        </div>
        <ul className="space-y-2 text-gray-300 ml-4">
          <li>Auto-rewrite VO/сабів</li>
          <li>Re-render pipeline</li>
        </ul>
      </div>
      <div className="bg-orange-500/20 rounded-xl p-6 border-l-4 border-orange-500">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-2xl font-semibold text-white">Тиждень 4: Advanced Features</h3>
          <span className="text-orange-400 font-bold">Nice to have</span>
        </div>
        <ul className="space-y-2 text-gray-300 ml-4">
          <li>CTR/CVR predictions</li>
          <li>A/B варіації</li>
          <li>Enhanced UI/UX</li>
        </ul>
      </div>
    </div>
  </div>
);

export const roadmapSlideConfig = {
  title: "Roadmap",
  bg: "bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900"
};