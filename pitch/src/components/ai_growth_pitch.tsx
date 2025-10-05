import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Zap, DollarSign, Shield, TrendingUp, Clock, Target, CheckCircle, AlertTriangle } from 'lucide-react';

const Presentation = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    // Slide 1: Title
    {
      title: "AI Growth Strategist",
      subtitle: "Від брифу до креативів за хвилини, не за тижні",
      bg: "bg-gradient-to-br from-purple-900 via-blue-900 to-black",
      content: (
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
      )
    },

    // Slide 2: Problem
    {
      title: "Проблема",
      bg: "bg-gradient-to-br from-red-900 to-gray-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-12">Креативне виробництво = найдорожча пляшка</h2>
          <div className="grid grid-cols-1 gap-6">
            <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
              <div className="flex items-start gap-4">
                <Clock className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-2xl font-semibold text-white mb-2">Повільно</h3>
                  <p className="text-gray-300 text-lg">Бриф → референси → сценарії → озвучка → монтаж → узгодження займає тижні</p>
                </div>
              </div>
            </div>
            <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
              <div className="flex items-start gap-4">
                <DollarSign className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-2xl font-semibold text-white mb-2">Дорого</h3>
                  <p className="text-gray-300 text-lg">Вартість однієї варіації: $500-2000. Масштабування потребує великої команди</p>
                </div>
              </div>
            </div>
            <div className="bg-red-800/30 border-l-4 border-red-500 p-6 rounded-r-lg">
              <div className="flex items-start gap-4">
                <AlertTriangle className="w-8 h-8 text-red-400 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-2xl font-semibold text-white mb-2">Ризиковано</h3>
                  <p className="text-gray-300 text-lg">20-40% креативів отримують бани/попередження → втрата бюджету та часу</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 3: Solution
    {
      title: "Рішення",
      bg: "bg-gradient-to-br from-green-900 to-blue-900",
      content: (
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
      )
    },

    // Slide 4: How it works - Step 1
    {
      title: "Step 1: Pattern Mining",
      bg: "bg-gradient-to-br from-blue-900 to-indigo-900",
      content: (
        <div className="space-y-6">
          <div className="bg-blue-500/20 rounded-xl p-2 inline-block">
            <span className="text-blue-400 font-bold text-xl px-4">STEP 1</span>
          </div>
          <h2 className="text-5xl font-bold text-white">Pattern Mining з реальних кейсів</h2>
          <div className="grid grid-cols-2 gap-6 mt-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-blue-500/30">
              <h3 className="text-2xl font-semibold text-blue-400 mb-4">Джерела</h3>
              <ul className="space-y-3 text-gray-300 text-lg">
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  Meta Ad Library
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  TikTok Creative Center
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  Successful campaigns
                </li>
              </ul>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-purple-500/30">
              <h3 className="text-2xl font-semibold text-purple-400 mb-4">Аналіз</h3>
              <ul className="space-y-3 text-gray-300 text-lg">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  Hook структура
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  Емоційна дуга
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  CTA паттерни
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  Візуальний стиль
                </li>
              </ul>
            </div>
          </div>
          <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-6 border border-blue-400/30 mt-8">
            <p className="text-xl text-white font-semibold">
              💡 Результат: База патернів з реальних, успішних оголошень — не випадкова генерація
            </p>
          </div>
        </div>
      )
    },

    // Slide 5: How it works - Step 2
    {
      title: "Step 2: Chat MVP Pro",
      bg: "bg-gradient-to-br from-purple-900 to-pink-900",
      content: (
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
            <p className="text-lg text-white flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-green-400" />
              <span className="font-semibold">✅ Вже реалізовано: Chat MVP Pro повністю працює</span>
            </p>
          </div>
        </div>
      )
    },

    // Slide 6: How it works - Step 3
    {
      title: "Step 3: Policy Preflight",
      bg: "bg-gradient-to-br from-orange-900 to-red-900",
      content: (
        <div className="space-y-6">
          <div className="bg-orange-500/20 rounded-xl p-2 inline-block">
            <span className="text-orange-400 font-bold text-xl px-4">STEP 3</span>
          </div>
          <h2 className="text-5xl font-bold text-white">Policy Checker + Auto Fix-it</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-orange-500/30">
              <h3 className="text-2xl font-semibold text-orange-400 mb-4 flex items-center gap-3">
                <Shield className="w-7 h-7" />
                Перевірка ризиків
              </h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Health claims
                </li>
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Бренди/логотипи
                </li>
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Музичні права
                </li>
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Чутливі теми
                </li>
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Знаменитості
                </li>
                <li className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  NSFW контент
                </li>
              </ul>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-green-500/30">
              <h3 className="text-2xl font-semibold text-green-400 mb-4 flex items-center gap-3">
                <Zap className="w-7 h-7" />
                Auto Fix-it
              </h3>
              <div className="space-y-4 text-gray-300">
                <p className="text-lg">Автоматичні пропозиції безпечних формулювань:</p>
                <div className="bg-red-500/20 p-3 rounded border-l-4 border-red-500">
                  <p className="text-sm text-gray-400">❌ Ризиковано:</p>
                  <p className="font-mono">"Гарантовано схуднете"</p>
                </div>
                <div className="bg-green-500/20 p-3 rounded border-l-4 border-green-500">
                  <p className="text-sm text-gray-400">✅ Безпечно:</p>
                  <p className="font-mono">"Може допомогти досягти цілей"</p>
                </div>
                <p className="text-sm text-green-400 mt-4">+ автоматичний re-render з фіксами</p>
              </div>
            </div>
          </div>
          <div className="bg-green-500/20 rounded-xl p-4 border border-green-400/30">
            <p className="text-lg text-white flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-green-400" />
              <span className="font-semibold">✅ Policy Checker реалізований та працює</span>
            </p>
          </div>
        </div>
      )
    },

    // Slide 7: Value Proposition
    {
      title: "Цінність для бізнесу",
      bg: "bg-gradient-to-br from-green-900 via-emerald-900 to-teal-900",
      content: (
        <div className="space-y-8">
          <h2 className="text-5xl font-bold text-white mb-8">Чому це важливо?</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-8 border border-green-400/30">
              <Clock className="w-12 h-12 text-green-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-3">Швидше</h3>
              <p className="text-gray-300 text-lg mb-2">Time-to-market:</p>
              <div className="flex items-center gap-4">
                <span className="text-red-400 line-through text-xl">7-14 днів</span>
                <span className="text-4xl">→</span>
                <span className="text-green-400 font-bold text-2xl">2-4 години</span>
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl p-8 border border-blue-400/30">
              <DollarSign className="w-12 h-12 text-blue-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-3">Дешевше</h3>
              <p className="text-gray-300 text-lg mb-2">Cost per variation:</p>
              <div className="text-center mt-4">
                <div className="text-5xl font-bold text-blue-400">-70%</div>
                <p className="text-gray-400 mt-2">економія на виробництві</p>
              </div>
            </div>
            <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-8 border border-purple-400/30">
              <Shield className="w-12 h-12 text-purple-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-3">Безпечніше</h3>
              <p className="text-gray-300 text-lg mb-2">Рівень банів:</p>
              <div className="flex items-center gap-4">
                <span className="text-red-400 line-through text-xl">20-40%</span>
                <span className="text-4xl">→</span>
                <span className="text-green-400 font-bold text-2xl">&lt;5%</span>
              </div>
            </div>
            <div className="bg-gradient-to-br from-orange-500/20 to-yellow-500/20 rounded-xl p-8 border border-orange-400/30">
              <TrendingUp className="w-12 h-12 text-orange-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-3">Масштабніше</h3>
              <p className="text-gray-300 text-lg mb-2">Продуктивність:</p>
              <div className="text-center mt-4">
                <div className="text-5xl font-bold text-orange-400">100+</div>
                <p className="text-gray-400 mt-2">варіацій на тиждень без росту команди</p>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 8: Unique Advantages
    {
      title: "Унікальні переваги",
      bg: "bg-gradient-to-br from-indigo-900 to-purple-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Чим відрізняємось від конкурентів?</h2>
          <div className="space-y-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-blue-500">
              <h3 className="text-2xl font-semibold text-blue-400 mb-2">🎯 Патерни з реальних оголошень</h3>
              <p className="text-gray-300 text-lg">Не абстрактна генерація — база успішних кейсів з Meta Ad Library, TikTok Creative Center</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-purple-500">
              <h3 className="text-2xl font-semibold text-purple-400 mb-2">🧠 Deep Analysis</h3>
              <p className="text-gray-300 text-lg">Психологічні тригери, емоційна дуга, гіпотези для A/B тестування</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-green-500">
              <h3 className="text-2xl font-semibold text-green-400 mb-2">🛡️ Comprehensive Policy Check</h3>
              <p className="text-gray-300 text-lg">Не просто детекція — конкретні action items і автоматичні фікси</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-orange-500">
              <h3 className="text-2xl font-semibold text-orange-400 mb-2">🔄 Fix-it Chain</h3>
              <p className="text-gray-300 text-lg">Від виявлення ризику → переписаний VO/саби → автоматичний re-render</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-l-4 border-pink-500">
              <h3 className="text-2xl font-semibold text-pink-400 mb-2">📱 Platform-Native</h3>
              <p className="text-gray-300 text-lg">Автоматична адаптація форматів, шрифтів, CTA під кожну платформу</p>
            </div>
          </div>
        </div>
      )
    },

    // Slide 9: Technical Status
    {
      title: "Поточний статус",
      bg: "bg-gradient-to-br from-teal-900 to-cyan-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Що вже працює?</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-3xl font-semibold text-green-400 mb-4">✅ Готово</h3>
              <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Step 1: Pattern Mining</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• Парсинг оголошень</li>
                  <li>• Аналіз компонентів</li>
                  <li>• HTML звіти з інсайтами</li>
                </ul>
              </div>
              <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Step 2: Chat MVP Pro</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• Conversational UI</li>
                  <li>• Pattern suggestions</li>
                  <li>• Platform presets</li>
                  <li>• Session management</li>
                </ul>
              </div>
              <div className="bg-green-500/20 rounded-xl p-6 border border-green-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Step 3: Policy Checker</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• Risk detection</li>
                  <li>• Action items</li>
                  <li>• HTML reports</li>
                </ul>
              </div>
            </div>
            <div className="space-y-4">
              <h3 className="text-3xl font-semibold text-blue-400 mb-4">🚧 В розробці</h3>
              <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Video Generation</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• TTS озвучка</li>
                  <li>• FFmpeg монтаж</li>
                  <li>• S3 upload</li>
                </ul>
              </div>
              <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Global Patterns DB</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• Семантичний пошук</li>
                  <li>• Крос-кейсовий аналіз</li>
                </ul>
              </div>
              <div className="bg-blue-500/20 rounded-xl p-6 border border-blue-400/30">
                <h4 className="text-xl font-semibold text-white mb-2">Fix-it Automation</h4>
                <ul className="space-y-2 text-gray-300">
                  <li>• Auto-rewrite VO</li>
                  <li>• Auto re-render</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 10: Demo Flow
    {
      title: "Демо флоу",
      bg: "bg-gradient-to-br from-violet-900 to-fuchsia-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Як це виглядає для користувача?</h2>
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-violet-400/30">
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">1</div>
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold text-white">Діалог з системою</h3>
                  <p className="text-gray-300 text-lg">"Хочу рекламувати фітнес-додаток для зайнятих професіоналів"</p>
                </div>
              </div>
              <div className="border-l-4 border-violet-400 ml-8 pl-8 space-y-3 text-gray-300">
                <p>Система: "Які основні фічі додатку?"</p>
                <p>Система: "Яка цільова аудиторія? Який головний біль вирішуєте?"</p>
                <p>Система показує приклади успішних фітнес-креативів з бази патернів</p>
              </div>
              <div className="flex items-center gap-4 mt-6">
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">2</div>
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold text-white">Вибір платформ і форматів</h3>
                  <p className="text-gray-300 text-lg">Instagram Reels + TikTok, 15-30 сек, 3 варіації</p>
                </div>
              </div>
              <div className="flex items-center gap-4 mt-6">
                <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">3</div>
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold text-white">Генерація + Policy Check</h3>
                  <p className="text-gray-300 text-lg">Система генерує креативи та автоматично перевіряє на ризики</p>
                </div>
              </div>
              <div className="flex items-center gap-4 mt-6">
                <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">4</div>
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold text-white">Результат</h3>
                  <p className="text-gray-300 text-lg">ZIP-архів з відео, сабами, скриптами + звіт про безпечність</p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-xl p-6 border border-green-400/30 mt-6">
            <p className="text-xl text-white font-semibold text-center">
              Час виконання: 5-15 хвилин замість 7-14 днів
            </p>
          </div>
        </div>
      )
    },

    // Slide 11: Market Context
    {
      title: "Universe Group Context",
      bg: "bg-gradient-to-br from-yellow-900 via-orange-900 to-red-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Чому Universe Group?</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-yellow-400/30">
              <h3 className="text-2xl font-semibold text-yellow-400 mb-4">Досвід масштабування</h3>
              <div className="space-y-3 text-gray-300">
                <p className="text-lg"><span className="font-bold text-white">200M+</span> користувачів</p>
                <p className="text-lg"><span className="font-bold text-white">180</span> країн світу</p>
                <p className="text-lg"><span className="font-bold text-white">3200+</span> людей у команді</p>
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-orange-400/30">
              <h3 className="text-2xl font-semibold text-orange-400 mb-4">Успішні продукти</h3>
              <div className="space-y-2 text-gray-300">
                <p>Cleaner Guru: 27M+ downloads</p>
                <p>Scan Guru: 35M+ downloads</p>
                <p>Visify: 2.5M downloads, 5M+ AI generations</p>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-8 border border-blue-400/30 mt-8">
            <h3 className="text-3xl font-bold text-white mb-4">Чому це важливо для нас?</h3>
            <div className="grid grid-cols-2 gap-6 text-lg text-gray-300">
              <div>
                <Target className="w-8 h-8 text-blue-400 mb-2" />
                <p>Витрачаємо мільйони $ на UA</p>
                <p className="text-sm text-gray-400 mt-1">Креативи = критичний bottleneck</p>
              </div>
              <div>
                <TrendingUp className="w-8 h-8 text-purple-400 mb-2" />
                <p>Потрібно 100+ варіацій/тиждень</p>
                <p className="text-sm text-gray-400 mt-1">Поточна команда не масштабується</p>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 12: Roadmap
    {
      title: "Roadmap",
      bg: "bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900",
      content: (
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
      )
    },

    // Slide 13: Competitive Advantage
    {
      title: "Конкурентна позиція",
      bg: "bg-gradient-to-br from-red-900 to-pink-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Порівняння з ринком</h2>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-white/20">
                  <th className="pb-4 text-xl text-gray-400">Функція</th>
                  <th className="pb-4 text-xl text-center text-gray-400">AdCreative.ai</th>
                  <th className="pb-4 text-xl text-center text-gray-400">Pencil</th>
                  <th className="pb-4 text-xl text-center text-green-400">AI Growth Strategist</th>
                </tr>
              </thead>
              <tbody className="text-lg">
                <tr className="border-b border-white/10">
                  <td className="py-4 text-white">Генерація креативів</td>
                  <td className="py-4 text-center text-green-400">✓</td>
                  <td className="py-4 text-center text-green-400">✓</td>
                  <td className="py-4 text-center text-green-400 font-bold">✓</td>
                </tr>
                <tr className="border-b border-white/10">
                  <td className="py-4 text-white">Патерни з реальних ads</td>
                  <td className="py-4 text-center text-red-400">✗</td>
                  <td className="py-4 text-center text-yellow-400">~</td>
                  <td className="py-4 text-center text-green-400 font-bold">✓</td>
                </tr>
                <tr className="border-b border-white/10">
                  <td className="py-4 text-white">Policy Checker</td>
                  <td className="py-4 text-center text-red-400">✗</td>
                  <td className="py-4 text-center text-yellow-400">Basic</td>
                  <td className="py-4 text-center text-green-400 font-bold">Advanced</td>
                </tr>
                <tr className="border-b border-white/10">
                  <td className="py-4 text-white">Auto Fix-it</td>
                  <td className="py-4 text-center text-red-400">✗</td>
                  <td className="py-4 text-center text-red-400">✗</td>
                  <td className="py-4 text-center text-green-400 font-bold">✓</td>
                </tr>
                <tr className="border-b border-white/10">
                  <td className="py-4 text-white">Deep Analysis</td>
                  <td className="py-4 text-center text-yellow-400">Basic</td>
                  <td className="py-4 text-center text-yellow-400">Basic</td>
                  <td className="py-4 text-center text-green-400 font-bold">Advanced</td>
                </tr>
                <tr>
                  <td className="py-4 text-white">Platform optimization</td>
                  <td className="py-4 text-center text-yellow-400">Manual</td>
                  <td className="py-4 text-center text-green-400">✓</td>
                  <td className="py-4 text-center text-green-400 font-bold">Auto</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-xl p-6 border border-green-400/30">
            <p className="text-xl text-white font-semibold">
              Наша перевага: Повний end-to-end цикл від pattern mining до policy-safe креативів
            </p>
          </div>
        </div>
      )
    },

    // Slide 14: Business Model
    {
      title: "Go-to-Market",
      bg: "bg-gradient-to-br from-cyan-900 to-blue-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Стратегія виходу на ринок</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-cyan-400/30">
              <h3 className="text-2xl font-semibold text-cyan-400 mb-4">Цільова аудиторія</h3>
              <ul className="space-y-3 text-gray-300 text-lg">
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
                  <span>Performance marketing teams у продуктових компаніях</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
                  <span>Digital marketing агентства</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
                  <span>DTC бренди з high-volume UA</span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2"></div>
                  <span>Mobile app developers</span>
                </li>
              </ul>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-blue-400/30">
              <h3 className="text-2xl font-semibold text-blue-400 mb-4">Ціноутворення</h3>
              <div className="space-y-4 text-gray-300">
                <div className="bg-blue-500/20 p-4 rounded-lg">
                  <p className="font-semibold text-white mb-1">Starter</p>
                  <p className="text-2xl font-bold text-blue-400">$299/міс</p>
                  <p className="text-sm">50 креативів, базовий policy check</p>
                </div>
                <div className="bg-blue-500/30 p-4 rounded-lg border border-blue-400">
                  <p className="font-semibold text-white mb-1">Pro</p>
                  <p className="text-2xl font-bold text-blue-400">$999/міс</p>
                  <p className="text-sm">500 креативів, advanced analytics</p>
                </div>
                <div className="bg-blue-500/20 p-4 rounded-lg">
                  <p className="font-semibold text-white mb-1">Enterprise</p>
                  <p className="text-2xl font-bold text-blue-400">Custom</p>
                  <p className="text-sm">Unlimited, API access, dedicated support</p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-green-400/30 mt-6">
            <h3 className="text-2xl font-semibold text-green-400 mb-4">Канали</h3>
            <div className="grid grid-cols-3 gap-4 text-gray-300">
              <div className="text-center p-4 bg-green-500/20 rounded-lg">
                <p className="font-semibold text-white">Партнерства</p>
                <p className="text-sm mt-2">З агентствами та UA networks</p>
              </div>
              <div className="text-center p-4 bg-green-500/20 rounded-lg">
                <p className="font-semibold text-white">Спільноти</p>
                <p className="text-sm mt-2">Performance marketing groups</p>
              </div>
              <div className="text-center p-4 bg-green-500/20 rounded-lg">
                <p className="font-semibold text-white">Інтеграції</p>
                <p className="text-sm mt-2">Meta, TikTok, Google Ads</p>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 15: KPIs
    {
      title: "Метрики успіху",
      bg: "bg-gradient-to-br from-emerald-900 to-teal-900",
      content: (
        <div className="space-y-6">
          <h2 className="text-5xl font-bold text-white mb-8">Як вимірюємо успіх?</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-emerald-400/30">
              <Clock className="w-12 h-12 text-emerald-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-2">Time-to-First-Creative</h3>
              <div className="text-5xl font-bold text-emerald-400 my-4">&lt; 30 хв</div>
              <p className="text-gray-300">Від брифу до першого креатива</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-teal-400/30">
              <DollarSign className="w-12 h-12 text-teal-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-2">Cost per Variation</h3>
              <div className="text-5xl font-bold text-teal-400 my-4">$5-15</div>
              <p className="text-gray-300">Замість $500-2000</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-green-400/30">
              <Shield className="w-12 h-12 text-green-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-2">Policy Pass Rate</h3>
              <div className="text-5xl font-bold text-green-400 my-4">&gt; 95%</div>
              <p className="text-gray-300">Креативів без банів/warnings</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-blue-400/30">
              <TrendingUp className="w-12 h-12 text-blue-400 mb-4" />
              <h3 className="text-3xl font-bold text-white mb-2">Weekly Output</h3>
              <div className="text-5xl font-bold text-blue-400 my-4">100+</div>
              <p className="text-gray-300">Варіацій на команду з 2-3 людей</p>
            </div>
          </div>
        </div>
      )
    },

    // Slide 16: Call to Action
    {
      title: "Наступні кроки",
      bg: "bg-gradient-to-br from-purple-900 via-pink-900 to-red-900",
      content: (
        <div className="space-y-8">
          <h2 className="text-6xl font-bold text-white mb-12 text-center">Готові до запуску!</h2>
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-8 border border-green-400/30 text-center">
              <div className="text-6xl mb-4">✅</div>
              <h3 className="text-2xl font-bold text-white mb-3">70% готово</h3>
              <p className="text-gray-300">Pattern Mining, Chat MVP Pro, Policy Checker працюють</p>
            </div>
            <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl p-8 border border-blue-400/30 text-center">
              <div className="text-6xl mb-4">⚡</div>
              <h3 className="text-2xl font-bold text-white mb-3">2-4 тижні</h3>
              <p className="text-gray-300">До повного MVP з video generation</p>
            </div>
            <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-8 border border-purple-400/30 text-center">
              <div className="text-6xl mb-4">🚀</div>
              <h3 className="text-2xl font-bold text-white mb-3">Ready for pilot</h3>
              <p className="text-gray-300">Пошук партнера для тестування</p>
            </div>
          </div>
          <div className="bg-gradient-to-r from-yellow-500/30 to-orange-500/30 rounded-2xl p-10 border-2 border-yellow-400/50 mt-12">
            <h3 className="text-3xl font-bold text-white mb-6 text-center">Потребуємо:</h3>
            <div className="grid grid-cols-2 gap-6 text-lg text-gray-200">
              <div className="flex items-start gap-3">
                <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
                <span>Доступ до тестових ассетів і прикладів</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
                <span>Інфраструктура S3/GCS для зберігання</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
                <span>Партнер для пілоту (агентство/бренд)</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1" />
                <span>Feedback від performance команд</span>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 17: Final Slide
    {
      title: "Висновок",
      bg: "bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900",
      content: (
        <div className="text-center space-y-12">
          <h2 className="text-6xl font-bold text-white leading-tight">
            Від ідеї до безпечних креативів<br />за хвилини, не за тижні
          </h2>
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-12 border border-white/20 max-w-4xl mx-auto">
            <p className="text-3xl text-gray-200 leading-relaxed">
              <span className="text-blue-400 font-bold">Pattern mining</span> з реальних ads + <span className="text-purple-400 font-bold">AI генерація</span> + <span className="text-green-400 font-bold">Policy Fix-it</span> = стабільний конвеєр перформанс-креативів
            </p>
          </div>
          <div className="grid grid-cols-4 gap-6 max-w-5xl mx-auto mt-16">
            <div className="text-center">
              <div className="text-5xl font-bold text-green-400 mb-2">-70%</div>
              <div className="text-gray-300 text-lg">вартість</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-blue-400 mb-2">10x</div>
              <div className="text-gray-300 text-lg">швидше</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-purple-400 mb-2">95%+</div>
              <div className="text-gray-300 text-lg">pass rate</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-orange-400 mb-2">100+</div>
              <div className="text-gray-300 text-lg">креативів/тиждень</div>
            </div>
          </div>
          <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mt-16">
            AI Growth Strategist
          </div>
          <div className="text-xl text-gray-400">
            Universe Group Hackathon 2025
          </div>
        </div>
      )
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="w-full h-screen flex flex-col">
      {/* Main slide area */}
      <div className={`flex-1 ${slides[currentSlide].bg} p-12 flex items-center justify-center overflow-auto`}>
        <div className="w-full max-w-7xl">
          {slides[currentSlide].content}
        </div>
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

export default Presentation;