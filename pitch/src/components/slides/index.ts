export { TitleSlide, titleSlideConfig } from './TitleSlide';
export { ProblemSlide, problemSlideConfig } from './ProblemSlide';
export { SolutionSlide, solutionSlideConfig } from './SolutionSlide';
export { PatternMiningSlide, patternMiningSlideConfig } from './PatternMiningSlide';
export { ChatMVPSlide, chatMVPSlideConfig } from './ChatMVPSlide';
export { PolicySlide, policySlideConfig } from './PolicySlide';
export { ValueSlide, valueSlideConfig } from './ValueSlide';
export { AdvantagesSlide, advantagesSlideConfig } from './AdvantagesSlide';
export { StatusSlide, statusSlideConfig } from './StatusSlide';
export { DemoFlowSlide, demoFlowSlideConfig } from './DemoFlowSlide';
export { MarketContextSlide, marketContextSlideConfig } from './MarketContextSlide';
export { RoadmapSlide, roadmapSlideConfig } from './RoadmapSlide';
export { CompetitiveSlide, competitiveSlideConfig } from './CompetitiveSlide';
export { GoToMarketSlide, goToMarketSlideConfig } from './GoToMarketSlide';
export { KPIsSlide, kpisSlideConfig } from './KPIsSlide';
export { NextStepsSlide, nextStepsSlideConfig } from './NextStepsSlide';
export { FinalSlide, finalSlideConfig } from './FinalSlide';

// Slide configuration type
export interface SlideConfig {
  title: string;
  subtitle?: string;
  bg: string;
  content: React.ReactNode;
}