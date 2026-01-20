import spotify from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedspotify = addPrefix(spotify, prefix);
  addBase({ ...prefixedspotify });
};
