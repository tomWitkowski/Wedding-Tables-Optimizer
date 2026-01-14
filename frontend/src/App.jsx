import React, { useState, useEffect } from 'react';
import { Users, LayoutGrid, Info } from 'lucide-react';
import RelationsEditor from './pages/RelationsEditor';
import TablesViewer from './pages/TablesViewer';
import { loadExampleData } from './utils/api';

function App() {
  const [activeTab, setActiveTab] = useState('relations');
  const [guests, setGuests] = useState([]);
  const [config, setConfig] = useState({
    max_seats: 10,
    family_friends_not_score: -3,
    iterations: 200,
    seats: [[null]]
  });
  const [optimizationResult, setOptimizationResult] = useState(null);

  // Load example data on mount
  useEffect(() => {
    loadExampleData().then(data => {
      setGuests(data.guests);
      setConfig(prev => ({ ...prev, ...data.config }));
    });
  }, []);

  const tabs = [
    { id: 'relations', name: 'Macierz Relacji', icon: Users },
    { id: 'tables', name: 'Stoliki', icon: LayoutGrid },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Wedding Tables Optimizer
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Zoptymalizuj rozmieszczenie gości przy stolikach weselnych
              </p>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg border border-blue-200">
              <Info className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-900">
                {guests.length} gości
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs Navigation */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm
                    transition-colors duration-200
                    ${activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'relations' && (
          <RelationsEditor
            guests={guests}
            setGuests={setGuests}
            config={config}
            setConfig={setConfig}
          />
        )}
        {activeTab === 'tables' && (
          <TablesViewer
            guests={guests}
            config={config}
            setConfig={setConfig}
            optimizationResult={optimizationResult}
            setOptimizationResult={setOptimizationResult}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Wedding Tables Optimizer v2.0 - Optymalizacja stolików weselnych w oparciu o macierz relacji
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
