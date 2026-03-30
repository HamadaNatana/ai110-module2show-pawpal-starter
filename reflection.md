# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The first idea of the UML design should have the following: 
1) A way for the user to view the tasks to be done
2) Adding a certain task for a certain pet
3) Marking a task as completed
- What classes did you include, and what responsibilities did you assign to each?
There should be approximately 3 classes: Task,Pet, and user. Each of these classes is responsible for the following:
- Task: manage the tasks per pet and checks if it is need to be completed or not
- Pet: assigned an owner and task to be completed. 
- Owner: be assigned a number of pets to be owned and what needs to be done, time availability to leave pets, prefrences,etc... 
- Schedule: keeps tasks organized by seeing which tasks need to be done

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
I added a owner to schedule link so that an owner can see the schedule specifically madde for him
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers priority and time
- How did you decide which constraints mattered most?
I decided that priority matters first since these require the most attention

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler is more readable in terms of checking the conflicts using list comprehension, yet it takes worst case O(n^2)
- Why is that tradeoff reasonable for this scenario?
It is better since trying to use set intersection as it leads to an error, or would require a freeze on the pet class causing more complications
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I gave both claude and copilot detailed prompts highlighting the main goal, how it can be achieved, and what can be avoided
- What kinds of prompts or questions were most helpful?
The prompts where there were more details on what is needed to be done, it is more accurate

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
AI wanted to write a test where it proves itself correct even if it does it incorrectly
- How did you evaluate or verify what the AI suggested?
By skimming over the code and running it to verify the outcome
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
The recurring tasks for daily, weekly, and monthly tasks and conflicting time slots for tasks
- Why were these tests important?
To verify that the code works as desired. For the recurrence, we had to check if the task is assigned again after the desired time is over. And the conflicting checks if the confliction occurs only between the same pet in the overlapping time slots

**b. Confidence**

- How confident are you that your scheduler works correctly?
Somewhat confident.
- What edge cases would you test next if you had more time?
If the confliction of tasks seem to be repeated tasks
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
That i have a sorting and filtering algorithm ffor the schedule
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would redesign the scheduling feature to make it more pinpoint accuate
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
That AI is not a pure genius, sometimes it needs very handguided prompts and rejections to get the right answer