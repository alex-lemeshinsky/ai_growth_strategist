'use client';

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { PresentationQR } from './QRCode';
import {
  TitleSlide,
  titleSlideConfig,
  ProblemSlide,
  problemSlideConfig,
  SolutionSlide,
  solutionSlideConfig,
  PatternMiningSlide,
  patternMiningSlideConfig,
  ChatMVPSlide,
  chatMVPSlideConfig,
  PolicySlide,
  policySlideConfig,
  ValueSlide,
  valueSlideConfig,
  AdvantagesSlide,
  advantagesSlideConfig,
  StatusSlide,
  statusSlideConfig,
  DemoFlowSlide,
  demoFlowSlideConfig,
  MarketContextSlide,
  marketContextSlideConfig,
  RoadmapSlide,
  roadmapSlideConfig,
  CompetitiveSlide,
  competitiveSlideConfig,
  GoToMarketSlide,
  goToMarketSlideConfig,
  KPIsSlide,
  kpisSlideConfig,
  NextStepsSlide,
  nextStepsSlideConfig,
  LiveDemoSlide,
  liveDemoSlideConfig,
  FinalSlide,
  finalSlideConfig,
} from './slides';

interface Slide {
  title: string;
  subtitle?: string;
  bg: string;
  content: React.ReactNode;
}

const PitchPresentation = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides: Slide[] = [
    { ...titleSlideConfig, content: <TitleSlide /> },
    { ...problemSlideConfig, content: <ProblemSlide /> },
    { ...solutionSlideConfig, content: <SolutionSlide /> },
    { ...patternMiningSlideConfig, content: <PatternMiningSlide /> },
    { ...chatMVPSlideConfig, content: <ChatMVPSlide /> },
    { ...policySlideConfig, content: <PolicySlide /> },
    { ...valueSlideConfig, content: <ValueSlide /> },
    { ...advantagesSlideConfig, content: <AdvantagesSlide /> },
    { ...statusSlideConfig, content: <StatusSlide /> },
    { ...demoFlowSlideConfig, content: <DemoFlowSlide /> },
    { ...liveDemoSlideConfig, content: <LiveDemoSlide /> },
    { ...marketContextSlideConfig, content: <MarketContextSlide /> },
    { ...roadmapSlideConfig, content: <RoadmapSlide /> },
    { ...competitiveSlideConfig, content: <CompetitiveSlide /> },
    { ...goToMarketSlideConfig, content: <GoToMarketSlide /> },
    { ...kpisSlideConfig, content: <KPIsSlide /> },
    { ...nextStepsSlideConfig, content: <NextStepsSlide /> },
    { ...finalSlideConfig, content: <FinalSlide /> },
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight') {
        nextSlide();
      } else if (event.key === 'ArrowLeft') {
        prevSlide();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentSlide]);

  return (
    <div className="w-full h-screen flex flex-col">
      {/* Main slide area */}
      <div className={`flex-1 ${slides[currentSlide].bg} p-12 flex items-center justify-center overflow-auto relative`}>
        <div className="w-full max-w-7xl">
          {slides[currentSlide].content}
        </div>
        <PresentationQR position="top-right" size="xl" />
      </div>

      {/* Navigation */}
      <div className="bg-black/80 backdrop-blur-sm p-6 flex items-center justify-between border-t border-white/10">
        <button
          onClick={prevSlide}
          className="flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 rounded-lg transition-colors text-white font-semibold"
        >
          <ChevronLeft className="w-5 h-5" />
          Назад
        </button>

        <div className="flex items-center gap-4">
          <span className="text-white font-semibold text-lg">
            {currentSlide + 1} / {slides.length}
          </span>
          <div className="flex gap-2">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSlide(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === currentSlide
                    ? 'bg-blue-400 w-8'
                    : 'bg-white/30 hover:bg-white/50'
                }`}
              />
            ))}
          </div>
        </div>

        <button
          onClick={nextSlide}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors text-white font-semibold"
        >
          Далі
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default PitchPresentation;