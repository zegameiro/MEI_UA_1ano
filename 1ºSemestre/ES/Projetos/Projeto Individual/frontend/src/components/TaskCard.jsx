import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Divider,
  Spinner,
} from "@nextui-org/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { RiDeleteBin6Line } from "react-icons/ri";
import { FiEdit3 } from "react-icons/fi";
import { FaCheckCircle } from "react-icons/fa";
import { BiSolidError } from "react-icons/bi";

import { putUpdateTask, deleteTask } from "../api/taskActions";
import { formatTimestamp } from "../utils";
import { useUserStore } from "../stores/userStore";

const TaskCard = ({
  index,
  task,
  onOpen,
  setCurrentTask,
  setIsEdit,
  setIsLoading2,
}) => {
  const queryClient = useQueryClient();
  const credential = useUserStore((state) => state.credential) || false;

  const completeTaskMutation = useMutation({
    mutationKey: ["update-task", task.id],
    mutationFn: () => {
      setIsLoading2(true);
      task.is_completed = true;
      putUpdateTask(task, credential);
    },
    onSuccess: () => {
      setTimeout(() => {
        queryClient.invalidateQueries("getTasks");
        setIsLoading2(false);
      }, 1000);
    },
    onError: () => console.error("Failed to complete task"),
  });

  const deleteTaskMutation = useMutation({
    mutationKey: ["delete-task", task.id],
    mutationFn: () => deleteTask(task.id, credential),
    onSuccess: () => queryClient.invalidateQueries("getTasks"),
    onError: () => console.error("Failed to delete task"),
  });

  return (
    <Card
      className={`max-w-[500px] ${
        task.priority == "high"
          ? "ring-4 ring-danger"
          : task.priority == "medium"
          ? "ring-4 ring-warning"
          : "ring-4 ring-blue-500"
      }`}
      key={index}
    >
      <CardHeader className="flex flex-row justify-between items-center">
        <p className="text-lg font-semibold">{task.title}</p>
        {task.is_completed ? (
          <p className="flex flex-row items-center gap-1 text-success">
            <FaCheckCircle /> Completed
          </p>
        ) : (
          <p className="flex flex-row items-center gap-1 text-warning">
            <BiSolidError /> Not Completed
          </p>
        )}
      </CardHeader>
      <Divider />
      <CardBody>
        <div className="flex flex-col space-y-3">
          <p>{task.description}</p>
          <div className="flex flex-row space-x-10">
            <span>
              <h2 className="font-semibold text-sm">Created at</h2>{" "}
              {formatTimestamp(task.creation_date)}
            </span>
            <span>
              <h2 className="font-semibold text-sm">Deadline</h2>{" "}
              {task.deadline}
            </span>
          </div>
        </div>
      </CardBody>
      <Divider />
      <CardFooter
        className={!task.is_completed ? "justify-between" : "justify-end"}
      >
        {completeTaskMutation.isError || deleteTaskMutation.isError ? (
          <span className="flex flex-row gap-1 items-center text-error font-semibold">
            <BiSolidError /> Error
          </span>
        ) : completeTaskMutation.isPending || deleteTaskMutation.isPending ? (
          <span className="flex flex-row gap-2 justify-center w-full items-center text-primary font-semibold">
            <Spinner size="md" color="secondary" /> Loading
          </span>
        ) : (
          <>
            {!task.is_completed && (
              <Button
                color="success"
                className="text-md"
                variant="flat"
                size="sm"
                onClick={() => completeTaskMutation.mutate()}
              >
                <FaCheckCircle /> Complete Task
              </Button>
            )}
            <div className="flex flex-row gap-5">
              <Button
                color="primary"
                variant="light"
                onClick={() => {
                  setCurrentTask(task);
                  setIsEdit(true);
                  onOpen();
                }}
              >
                <FiEdit3 />
                Edit
              </Button>
              <Button
                color="danger"
                onClick={() => deleteTaskMutation.mutate()}
              >
                <RiDeleteBin6Line /> Delete
              </Button>
            </div>
          </>
        )}
      </CardFooter>
    </Card>
  );
};

export default TaskCard;
