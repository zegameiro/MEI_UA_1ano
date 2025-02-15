import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Textarea,
  Spinner,
  RadioGroup,
  Radio,
  DatePicker,
} from "@nextui-org/react";
import { useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { getLocalTimeZone, parseDate, today } from "@internationalized/date";

import { MdError } from "react-icons/md";
import { FaCircleCheck } from "react-icons/fa6";

import { postAddTask, putUpdateTask } from "../api/taskActions";
import { useUserStore } from "../stores/userStore";

const AddTaskModal = ({
  isOpen,
  onOpenChange,
  onClose,
  currentTask,
  isEdit,
  setIsEdit,
  setCurrentTask,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
    setValue,
    watch,
  } = useForm();
  const [selected, setSelected] = useState();
  const [taskDeadline, setTaskDeadline] = useState();
  const queryClient = useQueryClient();
  const credential = useUserStore((state) => state.credential) || false;

	console.log(currentTask)

  const onSubmit = (data) => {
    if (isEdit) {
      currentTask.title = data.title;
      currentTask.description = data.description;
      currentTask.priority = data.priority;
      currentTask.deadline = data.deadline;
    }

    addTaskMutation.mutate(isEdit ? currentTask : data);
  };

  const addTaskMutation = useMutation({
    mutationKey: ["addTask"],
    mutationFn: (data) =>
      isEdit ? putUpdateTask(data, credential) : postAddTask(data, credential),
    onSuccess: () => {
      setTimeout(() => {
        reset();
        addTaskMutation.reset();
				setCurrentTask(undefined);
        onClose();
        queryClient.invalidateQueries("getTasks");
      }, 1000);
    },
    onError: () => {
      console.error("Failed to add task");
      setTimeout(() => {
        onClose();
        reset();
        addTaskMutation.reset();
      }, 1000);
    },
  });

  useEffect(() => {
    if (isEdit && currentTask) {
			reset({
				title: currentTask.title,
				description: currentTask.description,
        priority: currentTask.priority,
        deadline: currentTask.deadline,
			});
      setSelected(currentTask.priority);
    }

    if (
      taskDeadline != undefined ||
      taskDeadline != null ||
      taskDeadline?.length > 0
    ) {
      const deadline_day = String(taskDeadline?.day).padStart(2, "0");
      const deadline_month = String(taskDeadline?.month).padStart(2, "0");

      const deadline_date = `${taskDeadline?.year}-${deadline_month}-${deadline_day}`;
      setValue("deadline", deadline_date, { shouldValidate: true });
    }
  }, [isEdit, taskDeadline, reset, currentTask]);

  return (
    <Modal
      isDismissable={false}
      isKeyboardDismissDisabled
      backdrop="opaque"
      isOpen={isOpen}
      onOpenChange={onOpenChange}
      hideCloseButton
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className="flex flex-col gap-1">
              {isEdit ? "Edit task" : "Add a new Task"}
            </ModalHeader>
            <form onSubmit={handleSubmit(onSubmit)}>
              <ModalBody className="space-y-3">
                <Input
                  {...register("title", {
                    required: "Missing title for the Task",
                    maxLength: {
                      value: 100,
                      message: "Max length is 100 characters",
                    },
                    minLength: {
                      value: 5,
                      message:
                        "Title is required to have at least 5 characters",
                    },
                  })}
                  isRequired
                  isClearable
                  isInvalid={errors.title}
                  label="Title"
                  color={errors.title ? "danger" : "primary"}
                  variant="underlined"
                  errorMessage={errors.title?.message}
                  placeholder="Enter a title for your task"
                  labelPlacement="outside"
                  defaultValue={isEdit ? currentTask?.title : ""}
                  onClear={() => console.log("input cleared")}
                />
                <Textarea
                  {...register("description", {
                    required: "Missing description for the Task",
                    maxLength: {
                      value: 1000,
                      message: "Max length is 1000 characters",
                    },
                    minLength: {
                      value: 10,
                      message: "Description must have at least 10 characters",
                    },
                  })}
                  isRequired
                  isInvalid={errors.description}
                  variant="underlined"
                  label="Description"
                  color={errors.description ? "danger" : "primary"}
                  errorMessage={errors.description?.message}
                  labelPlacement="outside"
                  defaultValue={isEdit ? currentTask?.description : ""}
                  placeholder="Enter a description for your task"
                />

                <DatePicker
                  {...register("deadline", {
                    required: "Missing deadline for task",
                  })}
                  isRequired
                  isInvalid={errors.deadline}
                  defaultValue={
                    isEdit ? parseDate(currentTask?.deadline) : undefined
                  }
                  color={errors.deadline ? "danger" : "primary"}
                  errorMessage={errors.deadline?.message}
                  label="Deadline"
                  variant="underlined"
                  labelPlacement="outside"
                  minValue={today(getLocalTimeZone())}
                  onChange={setTaskDeadline}
                  showMonthAndYearPickers
                />

                <RadioGroup
                  color={errors.priority ? "danger" : "primary"}
                  value={selected}
                  onValueChange={setSelected}
                  isInvalid={errors.priority}
                  errorMessage={errors.priority?.message}
                  label="Select the task priority"
                  orientation="horizontal"
                >
                  <Radio
                    {...register("priority", {
                      required: "Missing priority for the Task",
                    })}
                    onChange={(e) => setValue("priority", e.target?.value)}
                    value="low"
                  >
                    Low
                  </Radio>
                  <Radio
                    {...register("priority", {
                      required: "Missing priority for the Task",
                    })}
                    onChange={(e) => setValue("priority", e.target?.value)}
                    value="medium"
                  >
                    Medium
                  </Radio>
                  <Radio
                    {...register("priority", {
                      required: "Missing priority for the Task",
                    })}
                    onChange={(e) => setValue("priority", e.target?.value)}
                    value="high"
                  >
                    High
                  </Radio>
                </RadioGroup>
              </ModalBody>
              <ModalFooter>
                {addTaskMutation.isPending ? (
                  <span className="flex flex-row gap-2 justify-center w-full items-center text-primary font-semibold">
                    <Spinner size="md" color="secondary" /> Loading
                  </span>
                ) : addTaskMutation.isSuccess ? (
                  <span className="flex flex-row gap-1 w-full justify-center items-center text-success font-semibold">
                    <FaCircleCheck /> Task {isEdit ? "edited" : "added"} with
                    success
                  </span>
                ) : addTaskMutation.isError ? (
                  <span className="flex flex-row gap-1 w-full justify-center items-center text-error font-semibold">
                    <MdError className="text-lg" /> Error -{" "}
                    {addTaskMutation.error?.detail}
                  </span>
                ) : (
                  <>
                    <Button
                      color="danger"
                      variant="light"
                      onPress={onClose}
                      onClick={() => {
                        reset();
                        addTaskMutation.reset();
                        setSelected();
                        setIsEdit(false);
                        setCurrentTask(undefined);
                      }}
                    >
                      Close
                    </Button>
                    <Button color="secondary" type="submit">
                      {isEdit ? "Edit Task" : "Add Task"}
                    </Button>
                  </>
                )}
              </ModalFooter>
            </form>
          </>
        )}
      </ModalContent>
    </Modal>
  );
};

export default AddTaskModal;
