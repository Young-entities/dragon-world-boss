import { useContext } from 'react';
import { GameContext } from './gameContext';

export const useGameState = () => useContext(GameContext);
