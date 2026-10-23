import { IconArrowLeft } from '@tabler/icons-react';
import JetonBrand from './JetonBrand';
import ModeMenu from './ModeMenu';
import type { View } from './navigation';

export type PageHeaderProps = { view: View; onNavigate: (view: View) => void };

export default function PageHeader({ view, onNavigate }: PageHeaderProps) {
  return (
    <header className="jt-head">
      <JetonBrand />
      <div className="jt-pills">
        <button type="button" className="jt-pill jt-back" onClick={() => onNavigate('trainer')}>
          <IconArrowLeft size={16} aria-hidden="true" />Entraîneur
        </button>
        <ModeMenu current={view} onSelect={onNavigate} />
      </div>
    </header>
  );
}
