import { IconCrown, IconFlame, IconMoodHappy, IconTargetArrow, type Icon } from '@tabler/icons-react';
import { BADGES } from './progress';

export const BADGE_ICONES: Record<string, Icon> = {
  [BADGES.roiDuBouton]: IconCrown,
  [BADGES.chasseurDeTirages]: IconTargetArrow,
  [BADGES.serie]: IconFlame,
  [BADGES.chatouilleur]: IconMoodHappy,
};

export type BadgeToastProps = { badge: string };

export default function BadgeToast({ badge }: BadgeToastProps) {
  const Icone = BADGE_ICONES[badge] ?? IconCrown;
  const detail = badge === BADGES.roiDuBouton ? 'Badge débloqué, et une couronne pour Jeton' : 'Badge débloqué';
  return (
    <div className="jt-toast" role="status">
      <span className="jt-toast-ic"><Icone size={24} stroke={2} aria-hidden="true" /></span>
      <span>
        <span className="jt-toast-sub">{detail}</span>
        <span className="jt-toast-title">{badge}</span>
      </span>
    </div>
  );
}
