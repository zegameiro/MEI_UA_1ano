import { FaSquare } from "react-icons/fa";

const Legend = () => {
  return (
    <div className="flex flex-row space-x-5 py-4">
      <span className="flex flex-row items-center gap-2">
        <FaSquare className="text-blue-500" /> Low Priority
      </span>
      <span className="flex flex-row items-center gap-2">
        <FaSquare className="text-warning" /> Medium Priority
      </span>
      <span className="flex flex-row items-center gap-2">
        <FaSquare className="text-danger" /> High Priority
      </span>
    </div>
  );
};

export default Legend;
