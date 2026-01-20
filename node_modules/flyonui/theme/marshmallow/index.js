import marshmallow from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedmarshmallow = addPrefix(marshmallow, prefix);
  addBase({ ...prefixedmarshmallow });
};
