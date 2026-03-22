import React from 'react';
import { Card } from '../data/cards';
import './CardSelector.css';

interface CardSelectorProps {
  cards: Card[];
  onSelectCards: (cardIds: string[]) => void;
  selectedCards: string[];
}

export default function CardSelector({
  cards,
  onSelectCards,
  selectedCards
}: CardSelectorProps) {
  const handleCardClick = (index: number) => {
    const newCards = [...selectedCards];
    const currentCard = newCards[0];
    newCards.splice(0, 1);
    newCards.push(currentCard);
    [newCards[0], newCards[index]] = [newCards[index], newCards[0]];
    onSelectCards(newCards);
  };

  const totalHP = cards.reduce((sum, card) => sum + card.hp, 0);

  return (
    <div className="card-selector">
      <div className="hp-display">
        <div className="hp-bar">
          <div className="hp-fill" style={{ width: '100%' }}></div>
        </div>
        <p className="hp-text">Total HP: {totalHP}</p>
      </div>

      <div className="cards-container">
        {cards.map((card, index) => (
          <div
            key={index}
            className={`card ${index === 0 ? 'active' : ''}`}
            onClick={() => handleCardClick(index)}
            title={`Click to move to front`}
          >
            <div className="card-name">{card.name}</div>
            <div className="card-hp">❤️ {card.hp}</div>
            <div className="card-damages">
              <div className="damage-row">
                <span className="damage-label">R:</span>
                <span className="damage-value">{card.damageToRock}</span>
              </div>
              <div className="damage-row">
                <span className="damage-label">S:</span>
                <span className="damage-value">{card.damageToScissors}</span>
              </div>
              <div className="damage-row">
                <span className="damage-label">P:</span>
                <span className="damage-value">{card.damageToPaper}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
