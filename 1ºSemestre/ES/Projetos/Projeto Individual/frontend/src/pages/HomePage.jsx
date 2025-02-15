import {
  useDisclosure,
  Button,
  Spinner,
  Select,
  SelectItem,
} from "@nextui-org/react";
import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { PiGraph } from "react-icons/pi";

import AddTaskModal from "../components/AddTaskModal";
import { getTasks } from "../api/taskActions";
import TaskCard from "../components/TaskCard";
import Legend from "../components/Legend";
import { useFilterSortStore } from "../stores/filterStore";
import { useUserStore } from "../stores/userStore";

const HomePage = () => {
  const { isOpen, onOpen, onOpenChange, onClose } = useDisclosure();
  const queryClient = useQueryClient();

  const filterOption =
    useFilterSortStore((state) => state.filterOption) || false;
  const sortOption = useFilterSortStore((state) => state.sortOption) || false;
  const sortOrder = useFilterSortStore((state) => state.sortOrder) || false;
  const sortStore =
    useFilterSortStore((state) => state.setSortOptions) || false;
  const filterStore =
    useFilterSortStore((state) => state.setFilterOption) || false;

  const [currentTask, setCurrentTask] = useState();
  const [isEdit, setIsEdit] = useState(false);
  const [isLoading2, setIsLoading2] = useState(false);
  const credential = useUserStore((state) => state.credential) || false;

  const { data: tasks, isLoading: loadingTasks } = useQuery({
    queryKey: ["getTasks"],
    queryFn: () => getTasks(filterOption, sortOption, sortOrder, credential),
  });

  const handleFiltersChange = (e) => {
    setIsLoading2(true);
    filterStore(e.target.value);
    setTimeout(() => {
      queryClient.invalidateQueries("getTasks");
      setIsLoading2(false);
    }, 1000);
  };

  const handleSortChange = (e) => {
    setIsLoading2(true);
    let sort_opt = e.target.value.split("_");
    sortStore(sort_opt[0], sort_opt[1]);
    setTimeout(() => {
      queryClient.invalidateQueries("getTasks");
      setIsLoading2(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col">
      <div className="flex flex-row items-center justify-evenly">
        <h1 className="flex flex-row gap-2 items-center text-2xl font-bold">
          <PiGraph /> My Tasks
        </h1>
        <Button
          onPress={onOpen}
          onClick={() => {
            setIsEdit(false);
            setCurrentTask(undefined);
          }}
        >
          Add a new Task
        </Button>
      </div>
      <div className="flex flex-col pt-2">
        <Legend />
        <div className="flex flex-row space-x-5">
          <Select
            labelPlacement="outside"
            className="pb-5"
            variant="underlined"
            label="Filter Tasks"
            selectedKeys={[filterOption]}
            onChange={handleFiltersChange}
          >
            <SelectItem key="completed">Completed Tasks</SelectItem>
            <SelectItem key="not_completed">Incomplete Tasks</SelectItem>
            <SelectItem key="low_prio">Priority Low</SelectItem>
            <SelectItem key="medium_prio">Priority Medium</SelectItem>
            <SelectItem key="high_prio">Priority High</SelectItem>
          </Select>
          <Select
            labelPlacement="outside"
            className="pb-5"
            variant="underlined"
            label="Sort Tasks"
            selectedKeys={[`${sortOption}_${sortOrder}`]}
            onChange={handleSortChange}
          >
            <SelectItem key="title_asc">Title Asc.</SelectItem>
            <SelectItem key="title_desc">Title Desc.</SelectItem>
            <SelectItem key="completed_asc">Completed</SelectItem>
            <SelectItem key="completed_desc">Not Completed</SelectItem>
            <SelectItem key="priority_asc">Priority Asc.</SelectItem>
            <SelectItem key="priority_desc">Priority Desc.</SelectItem>
            <SelectItem key="creation_asc">Creation Date Asc.</SelectItem>
            <SelectItem key="creation_desc">Creation Date Desc.</SelectItem>
            <SelectItem key="deadline_asc">Deadline Asc.</SelectItem>
            <SelectItem key="deadline_desc">Deadline Desc.</SelectItem>
          </Select>
        </div>
      </div>
      <div className="flex flex-col py-5">
        <AddTaskModal
          isOpen={isOpen}
          onOpenChange={onOpenChange}
          onClose={onClose}
          currentTask={currentTask}
          isEdit={isEdit}
          setIsEdit={setIsEdit}
          setCurrentTask={setCurrentTask}
        />

        <div className="flex flex-col space-y-4">
          {loadingTasks || isLoading2 ? ( // The query is still being done
            <span className="flex flex-row gap-2 justify-center w-full items-center text-primary font-semibold">
              <Spinner size="md" color="secondary" /> Loading
            </span>
          ) : tasks && tasks?.data?.length > 0 ? ( // Show the list of tasks organized by cards
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {tasks.data.map((task, index) => (
                <TaskCard
                  key={index}
                  task={task}
                  onOpen={onOpen}
                  setCurrentTask={setCurrentTask}
                  setIsEdit={setIsEdit}
                  setIsLoading2={setIsLoading2}
                />
              ))}
            </div>
          ) : (
            // Default case no tasks were found
            <span>No Tasks where found</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
