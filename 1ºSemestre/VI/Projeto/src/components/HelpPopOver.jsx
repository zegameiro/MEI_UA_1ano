import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  Button,
  Divider
} from "@nextui-org/react";
import { LuHelpCircle } from "react-icons/lu";

const HelpPopHover = ({ information, placement }) => {
  return (
    <Popover className="dark text-white max-w-md" placement={placement}>
      <PopoverTrigger>
        <Button color="primary" className="flex flex-row items-center gap-2">Help <LuHelpCircle className="text-lg"/> </Button>
      </PopoverTrigger>
      <PopoverContent>
        <div className="px-1 py-2">
          {Object.entries(information).map(([key, value], index) => (
            <div key={index} className="flex flex-col">
              <span className="text-lg font-bold pb-2">{key}</span>
              {Array.isArray(value) ? (
                <ul className="list-disc ml-4 text-[#ccc]">
                  {value.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              ) : (
                <span className="text-[#ccc]">{value}</span>
              )}
              <Divider className="my-3" />
            </div>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default HelpPopHover;
