import { useData } from '../DataContext';
import All_set_xx from "./All_set_xx";
import Labs_data from "./Labs_data";

const LapPage= () => {

  const { labName } = useData();
  var render = ""
  if (labName !== 'ALL_SET01' && labName !== 'ALL_SET02'){
    render = Labs_data()
  }
  else {
    render = All_set_xx()
  }

return (
  render
);
}
export default LapPage;