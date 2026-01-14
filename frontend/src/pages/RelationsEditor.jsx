import React, { useState } from 'react';
import { Plus, Trash2, UserPlus, Upload, Download, HelpCircle } from 'lucide-react';

function RelationsEditor({ guests, setGuests, config, setConfig }) {
  const [selectedGuest, setSelectedGuest] = useState(null);
  const [newGuestName, setNewGuestName] = useState('');
  const [newGuestState, setNewGuestState] = useState('f');

  const addGuest = () => {
    if (!newGuestName.trim()) return;

    const newGuest = {
      person_id: guests.length > 0 ? Math.max(...guests.map(g => g.person_id)) + 1 : 0,
      state: newGuestState,
      relations: {},
      name: newGuestName.trim()
    };

    setGuests([...guests, newGuest]);
    setNewGuestName('');
  };

  const removeGuest = (guestId) => {
    setGuests(guests.filter(g => g.person_id !== guestId));
    // Remove relations to this guest from other guests
    setGuests(prev => prev.map(g => ({
      ...g,
      relations: Object.fromEntries(
        Object.entries(g.relations).filter(([id]) => parseInt(id) !== guestId)
      )
    })));
    if (selectedGuest?.person_id === guestId) {
      setSelectedGuest(null);
    }
  };

  const updateRelation = (fromGuestId, toGuestId, score) => {
    setGuests(prev => prev.map(g => {
      if (g.person_id === fromGuestId) {
        const newRelations = { ...g.relations };
        if (score === '' || score === null) {
          delete newRelations[toGuestId];
        } else {
          newRelations[toGuestId] = parseFloat(score);
        }
        return { ...g, relations: newRelations };
      }
      return g;
    }));
  };

  const exportData = () => {
    const dataStr = JSON.stringify(guests, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = 'wedding-guests.json';

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const importData = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          setGuests(data);
        } catch (error) {
          alert('Błąd wczytywania pliku: ' + error.message);
        }
      };
      reader.readAsText(file);
    }
  };

  const getRelationColor = (score) => {
    if (score >= 10) return 'bg-green-100 text-green-800 border-green-300';
    if (score >= 2) return 'bg-blue-100 text-blue-800 border-blue-300';
    if (score >= 0.5) return 'bg-sky-50 text-sky-700 border-sky-200';
    if (score >= 0) return 'bg-gray-50 text-gray-700 border-gray-200';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  const getRelationLabel = (score) => {
    if (score >= 10) return 'Para';
    if (score >= 2) return 'Przyjaciele';
    if (score >= 0.5) return 'Znajomi';
    if (score >= 0) return 'Słaba';
    return 'Konflikt';
  };

  return (
    <div className="space-y-6">
      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <HelpCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-blue-900">
            <p className="font-medium mb-1">Jak działa macierz relacji?</p>
            <ul className="list-disc list-inside space-y-1 text-blue-800">
              <li><strong>10</strong> - Para towarzysząca (muszą siedzieć razem)</li>
              <li><strong>2-9</strong> - Dobrzy przyjaciele</li>
              <li><strong>0.5-2</strong> - Znajomi</li>
              <li><strong>0</strong> - Obojętna relacja</li>
              <li><strong>Wartości ujemne</strong> - Konflikty (lepiej nie sadzać razem)</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Ustawienia Optymalizacji</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maks. miejsc przy stoliku
            </label>
            <input
              type="number"
              min="2"
              max="20"
              value={config.max_seats}
              onChange={(e) => setConfig({ ...config, max_seats: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Kara za mieszanie rodziny/znajomych
            </label>
            <input
              type="number"
              step="0.5"
              max="0"
              value={config.family_friends_not_score}
              onChange={(e) => setConfig({ ...config, family_friends_not_score: parseFloat(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Liczba iteracji
            </label>
            <input
              type="number"
              min="10"
              max="1000"
              step="10"
              value={config.iterations}
              onChange={(e) => setConfig({ ...config, iterations: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Add Guest Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Dodaj Gościa</h2>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Imię i nazwisko"
            value={newGuestName}
            onChange={(e) => setNewGuestName(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addGuest()}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <select
            value={newGuestState}
            onChange={(e) => setNewGuestState(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="f">Rodzina</option>
            <option value="z">Znajomi</option>
          </select>
          <button
            onClick={addGuest}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2 transition-colors"
          >
            <UserPlus className="w-4 h-4" />
            Dodaj
          </button>
        </div>
      </div>

      {/* Import/Export */}
      <div className="flex gap-3">
        <button
          onClick={exportData}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
        >
          <Download className="w-4 h-4" />
          Eksportuj dane
        </button>
        <label className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors cursor-pointer">
          <Upload className="w-4 h-4" />
          Importuj dane
          <input
            type="file"
            accept=".json"
            onChange={importData}
            className="hidden"
          />
        </label>
      </div>

      {/* Guests List and Relations Matrix */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Guests List */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            Lista Gości ({guests.length})
          </h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {guests.map((guest) => (
              <div
                key={guest.person_id}
                className={`flex items-center justify-between p-3 rounded-lg border-2 cursor-pointer transition-all ${
                  selectedGuest?.person_id === guest.person_id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedGuest(guest)}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${guest.state === 'f' ? 'bg-purple-500' : 'bg-blue-500'}`} />
                  <div>
                    <div className="font-medium">{guest.name || `Gość ${guest.person_id}`}</div>
                    <div className="text-xs text-gray-500">
                      {guest.state === 'f' ? 'Rodzina' : 'Znajomi'} • ID: {guest.person_id}
                    </div>
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    removeGuest(guest.person_id);
                  }}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Relations Editor */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            Relacje {selectedGuest && `- ${selectedGuest.name || `Gość ${selectedGuest.person_id}`}`}
          </h2>
          {selectedGuest ? (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {guests
                .filter(g => g.person_id !== selectedGuest.person_id)
                .map((guest) => {
                  const relationScore = selectedGuest.relations[guest.person_id] || '';
                  return (
                    <div key={guest.person_id} className="flex items-center gap-3">
                      <div className="flex-1">
                        <div className="font-medium text-sm">{guest.name || `Gość ${guest.person_id}`}</div>
                        <div className="text-xs text-gray-500">
                          {guest.state === 'f' ? 'Rodzina' : 'Znajomi'}
                        </div>
                      </div>
                      <input
                        type="number"
                        step="0.5"
                        placeholder="0"
                        value={relationScore}
                        onChange={(e) => updateRelation(selectedGuest.person_id, guest.person_id, e.target.value)}
                        className={`w-20 px-2 py-1 text-center border-2 rounded-md focus:ring-2 focus:ring-blue-500 ${
                          relationScore !== '' ? getRelationColor(parseFloat(relationScore)) : 'border-gray-300'
                        }`}
                      />
                      {relationScore !== '' && (
                        <span className="text-xs font-medium w-20 text-center">
                          {getRelationLabel(parseFloat(relationScore))}
                        </span>
                      )}
                    </div>
                  );
                })}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-12">
              Wybierz gościa z listy po lewej, aby edytować jego relacje
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default RelationsEditor;
