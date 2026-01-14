import React, { useState } from 'react';
import { Play, RotateCcw, TrendingUp, Table2, AlertCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

function TablesViewer({ guests, config, setConfig, optimizationResult, setOptimizationResult }) {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [error, setError] = useState(null);
  const [draggedGuest, setDraggedGuest] = useState(null);

  const runOptimization = async () => {
    setIsOptimizing(true);
    setError(null);

    try {
      // Prepare API request
      const requestData = guests.map(g => ({
        person_id: g.person_id,
        state: g.state,
        relations: g.relations
      }));

      const response = await axios.post('http://localhost:8000/api/', requestData, {
        params: {
          max_seats: config.max_seats,
          family_friends_not_score: config.family_friends_not_score,
          iterations: config.iterations,
          seats: config.seats
        }
      });

      setOptimizationResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Błąd optymalizacji');
    } finally {
      setIsOptimizing(false);
    }
  };

  const resetOptimization = () => {
    setOptimizationResult(null);
    setConfig({ ...config, seats: [[null]] });
  };

  const moveGuestToTable = (guestId, fromTableIndex, toTableIndex) => {
    if (!optimizationResult) return;

    const newTables = optimizationResult.tables.map(table => [...table]);

    // Remove guest from old table
    if (fromTableIndex !== null) {
      newTables[fromTableIndex] = newTables[fromTableIndex].filter(id => id !== guestId);
    }

    // Add to new table
    if (newTables[toTableIndex].length < config.max_seats) {
      newTables[toTableIndex].push(guestId);
    }

    // Remove empty tables
    const filteredTables = newTables.filter(table => table.length > 0);

    setOptimizationResult({
      ...optimizationResult,
      tables: filteredTables
    });
  };

  const getGuestById = (id) => guests.find(g => g.person_id === id);

  const getTableScore = (tableGuestIds) => {
    if (!tableGuestIds || tableGuestIds.length < 2) return 0;

    let totalScore = 0;
    let pairCount = 0;

    for (let i = 0; i < tableGuestIds.length; i++) {
      for (let j = i + 1; j < tableGuestIds.length; j++) {
        const guest1 = getGuestById(tableGuestIds[i]);
        const guest2 = getGuestById(tableGuestIds[j]);

        if (guest1 && guest2) {
          const score = guest1.relations[guest2.person_id] || 0;
          totalScore += score;
          pairCount++;
        }
      }
    }

    return pairCount > 0 ? totalScore / tableGuestIds.length : 0;
  };

  const getScoreColor = (score) => {
    if (score >= 2) return 'text-green-600';
    if (score >= 1) return 'text-blue-600';
    if (score >= 0) return 'text-gray-600';
    return 'text-red-600';
  };

  const getTableBorderColor = (score) => {
    if (score >= 2) return 'border-green-400';
    if (score >= 1) return 'border-blue-400';
    if (score >= 0) return 'border-gray-300';
    return 'border-red-400';
  };

  const chartData = optimizationResult?.score_history?.map((score, index) => ({
    iteration: index,
    score: score.toFixed(3)
  })) || [];

  return (
    <div className="space-y-6">
      {/* Control Panel */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Panel Optymalizacji</h2>
          {optimizationResult && (
            <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-lg border border-green-200">
              <TrendingUp className="w-5 h-5 text-green-600" />
              <span className="text-sm font-medium text-green-900">
                Wynik: {optimizationResult.score_history[optimizationResult.score_history.length - 1]?.toFixed(2)}
              </span>
            </div>
          )}
        </div>

        <div className="flex gap-3">
          <button
            onClick={runOptimization}
            disabled={isOptimizing || guests.length < 2}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
          >
            <Play className="w-5 h-5" />
            {isOptimizing ? 'Optymalizacja...' : 'Uruchom Optymalizację'}
          </button>

          {optimizationResult && (
            <button
              onClick={resetOptimization}
              className="flex items-center gap-2 px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors font-medium"
            >
              <RotateCcw className="w-5 h-5" />
              Reset
            </button>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}
      </div>

      {/* Optimization Progress Chart */}
      {optimizationResult && chartData.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Postęp Optymalizacji</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="iteration" label={{ value: 'Iteracja', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Wynik', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-3 gap-4 text-center">
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {optimizationResult.score_history[0]?.toFixed(2)}
              </div>
              <div className="text-xs text-gray-600">Wynik początkowy</div>
            </div>
            <div className="p-3 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {optimizationResult.score_history[optimizationResult.score_history.length - 1]?.toFixed(2)}
              </div>
              <div className="text-xs text-gray-600">Wynik końcowy</div>
            </div>
            <div className="p-3 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {((optimizationResult.score_history[optimizationResult.score_history.length - 1] -
                   optimizationResult.score_history[0]) /
                  Math.abs(optimizationResult.score_history[0]) * 100).toFixed(1)}%
              </div>
              <div className="text-xs text-gray-600">Poprawa</div>
            </div>
          </div>
        </div>
      )}

      {/* Tables Visualization */}
      {optimizationResult ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">
              Wizualizacja Stolików ({optimizationResult.tables.length} stolików)
            </h2>
            <div className="text-sm text-gray-600">
              Przeciągnij gości między stolikami, aby dostosować ręcznie
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {optimizationResult.tables.map((table, tableIndex) => {
              const tableScore = getTableScore(table);
              return (
                <div
                  key={tableIndex}
                  className={`bg-white rounded-lg shadow-md p-6 border-2 ${getTableBorderColor(tableScore)} transition-all`}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    if (draggedGuest) {
                      moveGuestToTable(draggedGuest.id, draggedGuest.fromTable, tableIndex);
                      setDraggedGuest(null);
                    }
                  }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Table2 className="w-5 h-5 text-gray-600" />
                      <h3 className="font-semibold">Stolik {tableIndex + 1}</h3>
                    </div>
                    <div className={`text-sm font-medium ${getScoreColor(tableScore)}`}>
                      ⭐ {tableScore.toFixed(2)}
                    </div>
                  </div>

                  <div className="space-y-2">
                    {table.map((guestId) => {
                      const guest = getGuestById(guestId);
                      if (!guest) return null;

                      return (
                        <div
                          key={guestId}
                          draggable
                          onDragStart={() => setDraggedGuest({ id: guestId, fromTable: tableIndex })}
                          onDragEnd={() => setDraggedGuest(null)}
                          className={`p-3 rounded-lg border-2 cursor-move transition-all ${
                            draggedGuest?.id === guestId
                              ? 'border-blue-500 bg-blue-50 opacity-50'
                              : 'border-gray-200 bg-gray-50 hover:border-gray-300'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full flex-shrink-0 ${
                              guest.state === 'f' ? 'bg-purple-500' : 'bg-blue-500'
                            }`} />
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-sm truncate">
                                {guest.name || `Gość ${guestId}`}
                              </div>
                              <div className="text-xs text-gray-500">
                                {guest.state === 'f' ? 'Rodzina' : 'Znajomi'}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <div className="mt-3 pt-3 border-t border-gray-200 text-xs text-gray-500">
                    {table.length} / {config.max_seats} miejsc
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Table2 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Brak wyników optymalizacji
          </h3>
          <p className="text-gray-500">
            Kliknij "Uruchom Optymalizację", aby wygenerować rozmieszczenie stolików
          </p>
        </div>
      )}
    </div>
  );
}

export default TablesViewer;
