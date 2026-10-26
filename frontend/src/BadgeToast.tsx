import { IconCrown, IconFlame, IconTargetArrow, type Icon } from '@tabler/icons-react';
import { BADGES } from './progress';

export const BADGE_ICONES: Record<string, Icon> = {
  [BADGES.roiDuBouton]: IconCrown,
  [BADGES.chasseurDeTirages]: IconTargetArrow,
  [BADGES.serie]: IconFlame,
};

export type BadgeToastProps = { badge: string };

export default function BadgeToast({ badge }: BadgeToastProps) {
  const Icone = BADGE_ICONES[badge] ?? IconCrown;
  return (
    <div className="jt-toast" role="status">
      <span className="jt-toast-ic"><Icone size={24} stroke={2} aria-hidden="true" /></span>
      <span>
        <span className="jt-toast-sub">Badge débloqué</span>
        <span className="jt-toast-title">{badge}</span>
      </span>
    </div>
  );
}
