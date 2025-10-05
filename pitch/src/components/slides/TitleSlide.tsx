import React from 'react';

export const TitleSlide = () => (
  <div className="text-center space-y-8">
    <div className="text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
      AI Growth Strategist
    </div>
    <div className="text-3xl text-gray-300 font-light">
      Від брифу до креативів за хвилини, не за тижні
    </div>
    <div className="text-xl text-gray-400 mt-12">
      Universe Group Hackathon 2025
    </div>
  </div>
);

export const titleSlideConfig = {
  title: "AI Growth Strategist",
  subtitle: "Від брифу до креативів за хвилини, не за тижні",
  bg: "bg-gradient-to-br from-purple-900 via-blue-900 to-black"
};