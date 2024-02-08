import concurrent.futures
import multiprocessing

def my_func(args):
    process_id, data = args
    # Your function logic here
    print(f"yay, my ID is: {process_id}")
    result = f"Process ID: {process_id}, Data: {data}"
    return result

def worker_initializer(process_id_list):
    global PROCESS_ID_LIST
    PROCESS_ID_LIST = process_id_list

def main():
    max_workers = 12
    population_size = 100
    population = [1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5,1, 2, 3, 4, 5]  # Your data goes here

    # Generate process IDs
    process_ids = list(range(max_workers))

    # Create a shared variable for process IDs
    with multiprocessing.Manager() as manager:
        process_id_list = manager.list(process_ids)

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, initializer=worker_initializer, initargs=(process_id_list,)) as executor:
            # Create population within the executor.map function
            results = list(executor.map(my_func,
                                        (
                                            (process_id, data) for process_id, data in zip(process_id_list * (population_size // max_workers + 1), population)
                                        )
                                        )
                           )

    # print(results)

if __name__ == "__main__":
    main()


