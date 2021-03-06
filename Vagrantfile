Vagrant.configure("2") do |config|

  config.vm.box = "centos/7"
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 1
  end

  N = 3
  (1..N).each do |machine_id|
    config.vm.define "machine#{machine_id}" do |machine|
      machine.vm.hostname = "machine#{machine_id}"
      machine.vm.network "private_network", ip: "192.168.77.#{20+machine_id}"

      if machine_id == 3
        machine.vm.network "forwarded_port", guest: 9090, host: 9090
        machine.vm.network "forwarded_port", guest: 3000, host: 3000
      end

      if machine_id == N
        machine.vm.provision :ansible do |ansible|
          ansible.limit = "all"
          ansible.playbook = "playbook.yml"
          ansible.groups = {
            "zookeeper"  => ["machine1"],
            "kafka"      => ["machine1"],
            "solution1"  => ["machine2"],
            "solution2"  => ["machine2"],
            "monitoring" => ["machine3"],
            "zookeeper:vars" => {
              "zookeeper_servers_list" => "server.1=192.168.77.21:2888:3888;2181",
            },
            "kafka:vars" => {
              "kafka_create_topics" => "input:10:1,output:10:1",
              "kafka_zookeeper_connect" => "192.168.77.21:2181,",
            }
          }
          ansible.host_vars = {
            "machine1" => {
              "zookeeper_id" => 1,
              "kafka_broker_id" => 1,
              "kafka_advertised_host_name" => "192.168.77.21",
            },
            "machine2" => {
              "solution1_kafka_topic" => "input",
              "solution1_kafka_bootstap_servers" => "192.168.77.21:9092",
              "solution2_kafka_input_topic" => "input",
              "solution2_kafka_output_topic" => "output",
              "solution2_kafka_bootstap_servers" => "192.168.77.21:9092",
            },
            "machine3" => {
              "kafka_exporter_arguments" => "--kafka.server=192.168.77.21:9092",
            }
          }
        end
      end
    end
  end
end
