import perplexity from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedperplexity = addPrefix(perplexity, prefix);
  addBase({ ...prefixedperplexity });
};
