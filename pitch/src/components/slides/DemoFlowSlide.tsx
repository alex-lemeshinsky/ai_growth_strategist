import React from 'react';

export const DemoFlowSlide = () => (
  <div className="space-y-6">
    <h2 className="text-5xl font-bold text-white mb-8">Як це виглядає для користувача?</h2>
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-violet-400/30">
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-purple-600 to-indigo-600 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">0</div>
          <div className="flex-1">
            <h3 className="text-2xl font-semibold text-white">Аналіз конкурентів</h3>
            <p className="text-gray-300 text-lg">Парсимо Meta Ad Library, видобуваємо паттерни з реальних оголошень</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">1</div>
          <div className="flex-1">
            <h3 className="text-2xl font-semibold text-white">Інтелектуальний діалог</h3>
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
            <h3 className="text-2xl font-semibold text-white">Пакет креативів</h3>
            <p className="text-gray-300 text-lg">Готові відео, саби, скрипти + детальний policy-звіт</p>
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
);

export const demoFlowSlideConfig = {
  title: "Демо флоу",
  bg: "bg-gradient-to-br from-violet-900 to-fuchsia-900"
};