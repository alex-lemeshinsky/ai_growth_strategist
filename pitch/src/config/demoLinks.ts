/**
 * Demo links configuration for CreatorFlow AI presentation
 * 
 * Update these URLs to point to actual demo instances
 */

export const DEMO_LINKS = {
  // Step 1: Pattern Mining Demo
  COMPETITOR_ANALYSIS_REPORT: "http://localhost:8000/report/task/177e59a6-c960-4b31-9740-231b91be231f",
  
  // Step 2: Chat MVP Demo  
  CHAT_DEMO: "http://localhost:8000/static/chat_pro.html?session_id=demo-session-123",
  
  // Step 3: Policy Checker Demo
  POLICY_REPORT: "http://localhost:8000/report/policy/demo-policy-task-456",
  
  // API Documentation
  API_DOCS: "http://localhost:8000/docs",
  
  // Additional demo resources
  GITHUB_REPO: "https://github.com/creators/creatorflow-ai",
  
} as const;

/**
 * Helper function to get demo link with fallback
 */
export const getDemoLink = (key: keyof typeof DEMO_LINKS, fallback?: string): string => {
  return DEMO_LINKS[key] || fallback || "#";
};

/**
 * Demo descriptions for each link
 */
export const DEMO_DESCRIPTIONS = {
  COMPETITOR_ANALYSIS_REPORT: "Інтерактивний HTML звіт з аналізом конкурентів, стратегіями та інсайтами",
  CHAT_DEMO: "Живий чат для збору брифу з персоналізованими рекомендаціями на основі аналізу",
  POLICY_REPORT: "Детальний policy звіт з рекомендаціями та action items",
  API_DOCS: "Повна документація API з можливістю тестування",
} as const;

/**
 * Check if running in development mode
 */
export const isDevelopment = () => {
  return process.env.NODE_ENV === 'development' || 
         window.location.hostname === 'localhost' || 
         window.location.hostname === '127.0.0.1';
};

/**
 * Get base URL for demos based on environment
 */
export const getBaseUrl = () => {
  if (isDevelopment()) {
    return "http://localhost:8000";
  }
  // Production URL would be here
  return "https://creatorflow-ai.demo.com";
};