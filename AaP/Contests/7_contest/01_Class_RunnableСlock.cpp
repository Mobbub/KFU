#include <vector>
#include <string>

class OSUpdater : public IRunnable 
{
public:
    void run() 
    {
        std::cout << "OSUpdater" << std::endl;
    }
};

class Alarm : public IRunnable 
{
public:
    void run() 
    {
        std::cout << "Alarm" << std::endl;
    }
};

class ActivityChecker : public IRunnable 
{
public:
    void run() 
    {
        std::cout << "ActivityChecker" << std::endl;
    }
};

class Clock : public IClock, public IRunnable 
{
private:
    struct Event 
    {
        IRunnable* client;
        Time time;
    };
    std::vector<Event> events;
public:
    void add(IRunnable* client, Time time) 
    {
        Event event;
        event.client = client;
        event.time = time;
        events.push_back(event);
    }
    std::string AddZero(short number)
    {
        if (number < 10)
        {
            return "0" + std::to_string(number);
        }
        else
        {
            return std::to_string(number);
        }
    }

    bool next() 
    {
        if (events.empty()) 
        {
            return false;
        }
        int nextIndex = 0;
        Time nextTime = events[0].time;
        for (int i = 1; i < events.size(); i++) 
        {
            if (events[i].time < nextTime) 
            {
                nextIndex = i;
                nextTime = events[i].time;
            }
        }
        std::cout << AddZero(nextTime.hours) << ":" << AddZero(nextTime.minutes) << ":" << AddZero(nextTime.seconds) << " ";
        events[nextIndex].client->run();
        events.erase(events.begin() + nextIndex);
        return true;
    }

    void run() 
    {
        while (next()) 
        {
        }
    }
};
