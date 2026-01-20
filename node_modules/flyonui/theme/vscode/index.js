import vscode from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedvscode = addPrefix(vscode, prefix);
  addBase({ ...prefixedvscode });
};
