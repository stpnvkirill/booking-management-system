import custombase from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedcustombase = addPrefix(custombase, prefix);
  addBase({ ...prefixedcustombase });
};
