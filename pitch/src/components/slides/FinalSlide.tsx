import React from 'react';

export const FinalSlide = () => (
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
);

export const finalSlideConfig = {
  title: "Висновок",
  bg: "bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900"
};