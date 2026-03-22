export type Hand = 'rock' | 'scissors' | 'paper';

export interface CardDamage {
  damageToRock: number;
  damageToScissors: number;
  damageToPaper: number;
}

export interface GameResult {
  winner: 'player1' | 'player2' | 'draw';
  damage: number;
  description: string;
}

export const determineWinner = (
  player1Hand: Hand,
  player2Hand: Hand,
  player1CardDamage: CardDamage,
  player2CardDamage: CardDamage
): GameResult => {
  // Check if it's a draw
  if (player1Hand === player2Hand) {
    return {
      winner: 'draw',
      damage: 0,
      description: 'Draw! No damage dealt.'
    };
  }

  // Rock beats Scissors, Scissors beats Paper, Paper beats Rock
  const winnerMap: Record<Hand, Hand> = {
    rock: 'scissors',
    scissors: 'paper',
    paper: 'rock'
  };

  if (winnerMap[player1Hand] === player2Hand) {
    // Player 1 wins with their hand, Player 2 takes damage
    const damageDealt = getDamage(player1Hand, player2CardDamage);
    return {
      winner: 'player1',
      damage: damageDealt,
      description: `Player 1 (${player1Hand}) beats Player 2 (${player2Hand})! ${damageDealt} damage dealt!`
    };
  } else {
    // Player 2 wins with their hand, Player 1 takes damage
    const damageDealt = getDamage(player2Hand, player1CardDamage);
    return {
      winner: 'player2',
      damage: damageDealt,
      description: `Player 2 (${player2Hand}) beats Player 1 (${player1Hand})! ${damageDealt} damage dealt!`
    };
  }
};

const getDamage = (winningHand: Hand, opponentCardDamage: CardDamage): number => {
  const damageMap: Record<Hand, keyof CardDamage> = {
    rock: 'damageToRock',
    scissors: 'damageToScissors',
    paper: 'damageToPaper'
  };

  const damageKey = damageMap[winningHand];
  return opponentCardDamage[damageKey];
};
