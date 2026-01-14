import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Optimize table seating arrangement
 * @param {import('../types').Guest[]} relations - Guest relations
 * @param {import('../types').OptimizationConfig} config - Optimization configuration
 * @returns {Promise<import('../types').OptimizationResult>}
 */
export async function optimizeTables(relations, config) {
  const response = await axios.post(`${API_BASE_URL}/api/`, relations, {
    params: config
  });
  return response.data;
}

/**
 * Export example data
 */
export async function loadExampleData() {
  // This would load from example_relations_request.json
  // For now, return sample data
  return {
    guests: [
      { person_id: 0, state: 'f', relations: { 1: 10, 2: 2 }, name: 'Jan Kowalski' },
      { person_id: 1, state: 'f', relations: { 0: 10, 3: 1 }, name: 'Anna Kowalska' },
      { person_id: 2, state: 'f', relations: { 0: 2, 3: 1 }, name: 'Piotr Nowak' },
      { person_id: 3, state: 'z', relations: { 1: 1, 2: 1, 4: 10 }, name: 'Ewa Nowak' },
      { person_id: 4, state: 'z', relations: { 3: 10, 5: 2 }, name: 'Marek Wiśniewski' },
      { person_id: 5, state: 'z', relations: { 4: 2, 6: 1 }, name: 'Kasia Dąbrowska' },
      { person_id: 6, state: 'z', relations: { 5: 1, 7: 10 }, name: 'Tomasz Lewandowski' },
      { person_id: 7, state: 'z', relations: { 6: 10 }, name: 'Maria Zielińska' },
    ],
    config: {
      max_seats: 4,
      family_friends_not_score: -3,
      iterations: 100
    }
  };
}
