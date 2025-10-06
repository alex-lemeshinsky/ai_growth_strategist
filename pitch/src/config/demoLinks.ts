/**
 * Demo links configuration for CreatorFlow AI presentation
 * 
 * Update these URLs to point to actual demo instances
 * Set NEXT_PUBLIC_API_BASE_URL environment variable to override the API base URL
 */

// Get API base URL from environment variable or fallback to localhost
const getApiBaseUrl = (): string => {
  // In browser environment, use the public environment variable
  if (typeof window !== 'undefined') {
    return (window as any).__ENV__?.NEXT_PUBLIC_API_BASE_URL || 
           process.env.NEXT_PUBLIC_API_BASE_URL || 
           'http://localhost:8000';
  }
  
  // Server-side environment
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

// Base URL for API calls
const API_BASE_URL = getApiBaseUrl();

export const DEMO_LINKS = {
  // Step 1: Pattern Mining Demo
  COMPETITOR_ANALYSIS_REPORT: `${API_BASE_URL}/report/task/177e59a6-c960-4b31-9740-231b91be231f`,
  
  // Step 2: Chat MVP Demo (static demo with AI recommendations)
  CHAT_DEMO: "/chat-mvp-demo.html",
  
  // Step 3: Policy Checker Demo
  POLICY_REPORT: `${API_BASE_URL}/report/policy/41f4074c-dc14-4266-bdaf-2b7edd8abac5`,
  
  // Step 4: Video Generation Demo
  VIDEO_DEMO: "https://cdn.shotstack.io/au/v1/qhwk4yr1p3/ef204875-40d5-43d0-bc98-adaa56778d7b.mp4",
  
  // API Documentation
  API_DOCS: `${API_BASE_URL}/docs`,
  
  // Additional demo resources
  GITHUB_REPO: "https://github.com/creators/creatorflow-ai",
  
} as const;

/**
 * Helper function to get demo link with fallback
 */
export const getDemoLink = (key: keyof typeof DEMO_LINKS, fallback?: string): string => {
  const link = DEMO_LINKS[key] || fallback || "#";
  
  // For relative paths, make them absolute with current presentation URL
  if (link.startsWith('/') && typeof window !== 'undefined') {
    return `${window.location.origin}${link}`;
  }
  
  return link;
};

/**
 * Demo descriptions for each link
 */
export const DEMO_DESCRIPTIONS = {
  COMPETITOR_ANALYSIS_REPORT: "Інтерактивний HTML звіт з аналізом конкурентів, стратегіями та інсайтами",
  CHAT_DEMO: "Статичний чат з готовими рекомендаціями ШІ та фінальним промптом для демонстрації",
  POLICY_REPORT: "Детальний policy звіт з рекомендаціями та action items",
  VIDEO_DEMO: "Приклад згенерованого відео креатива з TTS озвучкою та монтажем",
  API_DOCS: "Повна документація API з можливістю тестування",
  GITHUB_REPO: "Вихідний код проекту CreatorFlow AI на GitHub",
} as const;

/**
 * Check if running in development mode
 */
export const isDevelopment = () => {
  // Check if we're in browser environment first
  if (typeof window !== 'undefined') {
    return window.location.hostname === 'localhost' || 
           window.location.hostname === '127.0.0.1';
  }
  // Fallback for server-side
  return process.env.NODE_ENV === 'development';
};

/**
 * Get base URL for demos based on environment
 * @deprecated Use getApiBaseUrl instead
 */
export const getBaseUrl = () => {
  return getApiBaseUrl();
};

/**
 * Get current API base URL
 */
export { getApiBaseUrl };
