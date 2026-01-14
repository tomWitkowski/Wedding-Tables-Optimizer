/**
 * @typedef {'f' | 'z'} GuestState
 * f - family (rodzina)
 * z - friends (znajomi)
 */

/**
 * @typedef {Object} Guest
 * @property {number} person_id - Unique identifier
 * @property {GuestState} state - Family or friends
 * @property {Object.<number, number>} relations - Relations to other guests
 * @property {string} [name] - Optional display name
 */

/**
 * @typedef {Object} OptimizationConfig
 * @property {number[][]} seats - Initial seating arrangement
 * @property {number} family_friends_not_score - Penalty for mixing family and friends
 * @property {number} max_seats - Maximum seats per table
 * @property {number} iterations - Number of optimization iterations
 */

/**
 * @typedef {Object} OptimizationResult
 * @property {number[][]} tables - Optimized table arrangement
 * @property {number[]} tables_scores - Score for each table
 * @property {number[]} score_history - Optimization progress history
 */

export {};
