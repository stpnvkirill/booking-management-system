import Button from '@/shared/components/button/button';
// import { } from "@/shared/types/types"
import { FILTERS, type ActiveFilter } from '@/shared/types/types';

interface FilterProps {
  activeFilter?: ActiveFilter;
  setActiveFilter: React.Dispatch<
    React.SetStateAction<ActiveFilter | undefined>
  >;
}

export default function FilterBTNS({
  activeFilter = 'Все',
  setActiveFilter,
}: FilterProps) {
  return (
    <div className="mb-6">
      <h2 className="text-sm text-accent-content font-semibold mb-3">
        Фильтры
      </h2>
      <div className="flex gap-3 overflow-x-auto pb-2">
        {FILTERS.map((filter) => (
          <Button
            key={filter}
            label={`${filter}`}
            onClick={() => {
              setActiveFilter(filter);
            }}
            shape="rounded"
            size="xs"
            width="responsive"
            disabled={activeFilter === filter}
          />
        ))}
      </div>
    </div>
  );
}
