import claude from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedclaude = addPrefix(claude, prefix);
  addBase({ ...prefixedclaude });
};
