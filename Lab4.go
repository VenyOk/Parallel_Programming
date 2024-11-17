package main

import (
	"fmt"
	"math/rand"
	"os"
	"sync"
	"time"
)

const MAXT = 6000
const MINT = 1000
const PHIL_NUM = 5
const TIME = 20

func format_output(number int, act string) string {
	return fmt.Sprintf("Philosopher: %d\t action: %s", number, act)
}

func philosoph(number int, f []sync.Mutex, left int, right int, output chan string) {
	for {
		time_to_think := rand.Intn(MAXT + MINT)
		time_to_eat := rand.Intn(MAXT + MINT)
		output <- format_output(number, "think")
		time.Sleep(time.Duration(time_to_think) * time.Millisecond)
		output <- format_output(number, "wait")

		if number == PHIL_NUM {
			f[right-1].Lock()
			output <- format_output(number, fmt.Sprintf("took right fork with number = %d", right))
			f[left-1].Lock()
			output <- format_output(number, fmt.Sprintf("took left fork with number = %d", left))
		} else {
			f[left-1].Lock()
			output <- format_output(number, fmt.Sprintf("took left fork with number = %d", left))
			f[right-1].Lock()
			output <- format_output(number, fmt.Sprintf("took right fork with number = %d", right))
		}

		output <- format_output(number, "eat")
		time.Sleep(time.Duration(time_to_eat) * time.Millisecond)
		output <- format_output(number, "wait")
		f[right-1].Unlock()
		output <- format_output(number, fmt.Sprintf("put right fork with number = %d", right))
		f[left-1].Unlock()
		output <- format_output(number, fmt.Sprintf("put left fork with number = %d", left))
	}
}

func main() {
	output := make(chan string)
	f := make([]sync.Mutex, PHIL_NUM)
	for i := 1; i < PHIL_NUM; i++ {
		go philosoph(i, f, i, i+1, output)
	}
	go philosoph(PHIL_NUM, f, PHIL_NUM, 1, output)

	t := time.After(TIME * time.Second)
	for {
		select {
		case a := <-output:
			fmt.Println(a)
		case <-t:
			os.Exit(1)
		}
	}
}
